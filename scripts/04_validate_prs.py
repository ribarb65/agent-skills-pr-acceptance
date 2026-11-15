
from pathlib import Path
import duckdb

root = Path(__file__).resolve().parents[1]
con = duckdb.connect()

prs = root / "data/raw/aidev_v5_all_pr.parquet"

result = con.execute("""
SELECT
    COUNT(*) AS total_prs,
    COUNT(DISTINCT id) AS unique_prs,
    COUNT(*) FILTER (WHERE merged_at IS NOT NULL) AS merged_prs,
    COUNT(*) FILTER (
        WHERE closed_at IS NULL AND merged_at IS NULL
    ) AS open_prs,
    COUNT(*) FILTER (
        WHERE TRY_CAST(REPLACE(merged_at, 'Z', '') AS TIMESTAMP)
        < TRY_CAST(REPLACE(created_at, 'Z', '') AS TIMESTAMP)
    ) AS invalid_merge_dates
FROM read_parquet(?)
""", [str(prs)]).df()

print(result.to_string(index=False))

sample = root / "data/interim/phase0_usable_adopters.parquet"

result = con.execute("""
SELECT
    COUNT(*) AS repositories,
    COUNT(DISTINCT repo) AS unique_repositories,
    MIN(n_pre_adopt) AS minimum_pre_prs,
    MIN(n_post_adopt) AS minimum_post_prs
FROM read_parquet(?)
WHERE scope = 'v5/all'
AND date_status = 'complete'
AND n_post_adopt >= 5
""", [str(sample)]).df()

print(result.to_string(index=False))

con.close()
