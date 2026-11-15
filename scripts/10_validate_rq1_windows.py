
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
        LOWER(REPLACE(
            repo_url,
            'https://api.github.com/repos/',
            ''
        )) AS repo,
        TRY_CAST(
            REPLACE(created_at, 'Z', '') AS TIMESTAMP
        ) AS created_ts
    FROM read_parquet(?)
),
windows AS (
    SELECT
        c.repo,
        COUNT(p.id) FILTER (
            WHERE p.created_ts < c.adoption_ts
        ) AS pre_30,
        COUNT(p.id) FILTER (
            WHERE p.created_ts >= c.adoption_ts
        ) AS post_30
    FROM cohort c
    LEFT JOIN prs p
      ON p.repo = c.repo
     AND p.created_ts >= c.adoption_ts - INTERVAL 30 DAY
     AND p.created_ts < c.adoption_ts + INTERVAL 30 DAY
    GROUP BY c.repo
)
SELECT
    COUNT(*) AS repositories,
    SUM(pre_30) AS total_pre_prs,
    SUM(post_30) AS total_post_prs,
    COUNT(*) FILTER (WHERE pre_30 = 0) AS zero_pre,
    COUNT(*) FILTER (WHERE post_30 = 0) AS zero_post,
    COUNT(*) FILTER (
        WHERE pre_30 >= 1 AND post_30 >= 1
    ) AS at_least_one_each,
    COUNT(*) FILTER (
        WHERE pre_30 >= 5 AND post_30 >= 5
    ) AS at_least_five_each
FROM windows
""", [str(SAMPLE), str(PRS)]).df()

print(result.to_string(index=False))

con.close()
