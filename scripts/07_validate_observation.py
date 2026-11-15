
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/interim/phase0_usable_adopters.parquet"

con = duckdb.connect()

result = con.execute("""
SELECT
    COUNT(*) AS repositories,
    MIN(adoption_ts) AS first_adoption,
    MAX(adoption_ts) AS last_adoption,
    COUNT(*) FILTER (
        WHERE DATE_DIFF('day', adoption_ts, TIMESTAMP '2026-03-31 23:59:59') < 30
    ) AS under_30_days,
    COUNT(*) FILTER (
        WHERE DATE_DIFF('day', adoption_ts, TIMESTAMP '2026-03-31 23:59:59') < 60
    ) AS under_60_days,
    COUNT(*) FILTER (
        WHERE DATE_DIFF('day', adoption_ts, TIMESTAMP '2026-03-31 23:59:59') < 90
    ) AS under_90_days
FROM read_parquet(?)
WHERE scope = 'v5/all'
AND date_status = 'complete'
AND n_post_adopt >= 5
""", [str(SAMPLE)]).df()

print(result.to_string(index=False))

con.close()
