
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/interim/phase0_usable_adopters.parquet"
PRS = ROOT / "data/raw/aidev_v5_all_pr.parquet"

con = duckdb.connect()

result = con.execute("""
WITH cohort AS (
    SELECT repo, adoption_ts
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
      AND date_status = 'complete'
      AND n_pre_adopt >= 5
      AND adoption_ts <= TIMESTAMP '2026-03-31 23:59:59'
                             - INTERVAL 60 DAY
),
prs AS (
    SELECT
        id,
        LOWER(REPLACE(repo_url, 'https://api.github.com/repos/', '')) AS repo,
        TRY_CAST(REPLACE(created_at, 'Z', '') AS TIMESTAMP) AS created_ts,
        TRY_CAST(REPLACE(closed_at, 'Z', '') AS TIMESTAMP) AS closed_ts,
        TRY_CAST(REPLACE(merged_at, 'Z', '') AS TIMESTAMP) AS merged_ts
    FROM read_parquet(?)
),
window_prs AS (
    SELECT
        p.*,
        c.adoption_ts,
        CASE
            WHEN p.created_ts < c.adoption_ts THEN 'before'
            ELSE 'after'
        END AS period
    FROM cohort c
    JOIN prs p ON p.repo = c.repo
    WHERE p.created_ts >= c.adoption_ts - INTERVAL 30 DAY
      AND p.created_ts < c.adoption_ts + INTERVAL 30 DAY
),
outcomes AS (
    SELECT
        *,
        CASE
            WHEN merged_ts >= created_ts
             AND merged_ts < created_ts + INTERVAL 30 DAY
                THEN 'merged_30d'
            WHEN merged_ts IS NULL
             AND closed_ts >= created_ts
             AND closed_ts < created_ts + INTERVAL 30 DAY
                THEN 'closed_unmerged_30d'
            ELSE 'unresolved_30d'
        END AS outcome_30d
    FROM window_prs
)
SELECT
    period,
    COUNT(*) AS total_prs,
    COUNT(*) FILTER (
        WHERE outcome_30d = 'merged_30d'
    ) AS merged_30d,
    COUNT(*) FILTER (
        WHERE outcome_30d = 'closed_unmerged_30d'
    ) AS closed_unmerged_30d,
    COUNT(*) FILTER (
        WHERE outcome_30d = 'unresolved_30d'
    ) AS unresolved_30d,
    COUNT(*) FILTER (
        WHERE period = 'before'
          AND (
              merged_ts >= adoption_ts
              OR closed_ts >= adoption_ts
          )
    ) AS pre_prs_resolved_after_adoption,
    COUNT(*) FILTER (
        WHERE merged_ts > TIMESTAMP '2026-03-31 23:59:59'
           OR closed_ts > TIMESTAMP '2026-03-31 23:59:59'
    ) AS outcomes_after_cutoff
FROM outcomes
GROUP BY period
ORDER BY period DESC
""", [str(SAMPLE), str(PRS)]).df()

print(result.to_string(index=False))

for row in result.itertuples():
    assert row.total_prs == (
        row.merged_30d
        + row.closed_unmerged_30d
        + row.unresolved_30d
    )

con.close()
