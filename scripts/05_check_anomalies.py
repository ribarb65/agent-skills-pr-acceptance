
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
PRS = ROOT / "data/raw/aidev_v5_all_pr.parquet"
SAMPLE = ROOT / "data/interim/phase0_usable_adopters.parquet"

con = duckdb.connect()

result = con.execute("""
WITH invalid AS (
    SELECT
        id,
        LOWER(REGEXP_REPLACE(repo_url, '^https://api\\.github\\.com/repos/', '')) AS repo,
        TRY_CAST(REPLACE(created_at, 'Z', '') AS TIMESTAMP) AS created_ts,
        TRY_CAST(REPLACE(merged_at, 'Z', '') AS TIMESTAMP) AS merged_ts
    FROM read_parquet(?)
),
bad AS (
    SELECT *
    FROM invalid
    WHERE merged_ts < created_ts
),
selected AS (
    SELECT DISTINCT repo
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
      AND date_status = 'complete'
      AND n_post_adopt >= 5
)
SELECT
    COUNT(*) AS invalid_prs,
    COUNT(*) FILTER (
        WHERE selected.repo IS NOT NULL
    ) AS invalid_in_sample,
    MIN(DATE_DIFF('second', created_ts, merged_ts)) AS largest_negative_seconds
FROM bad
LEFT JOIN selected USING (repo)
""", [str(PRS), str(SAMPLE)]).df()

print(result.to_string(index=False))

con.close()
