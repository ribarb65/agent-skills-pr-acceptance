
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
PRS = ROOT / "data/raw/aidev_v5_all_pr.parquet"

con = duckdb.connect()

result = con.execute("""
SELECT
    state,
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE merged_at IS NOT NULL) AS merged,
    COUNT(*) FILTER (
        WHERE closed_at IS NOT NULL
        AND merged_at IS NULL
    ) AS closed_unmerged,
    COUNT(*) FILTER (
        WHERE closed_at IS NULL
        AND merged_at IS NULL
    ) AS open_prs,
    MIN(TRY_CAST(REPLACE(created_at, 'Z', '') AS TIMESTAMP)) AS first_pr,
    MAX(TRY_CAST(REPLACE(created_at, 'Z', '') AS TIMESTAMP)) AS last_pr
FROM read_parquet(?)
GROUP BY state
ORDER BY total DESC
""", [str(PRS)]).df()

print(result.to_string(index=False))

con.close()
