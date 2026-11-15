
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/interim/phase0_usable_adopters.parquet"

con = duckdb.connect()

result = con.execute("""
WITH candidates AS (
    SELECT
        repo,
        adoption_ts,
        n_pre_adopt,
        n_post_adopt
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
      AND date_status = 'complete'
      AND n_pre_adopt >= 5
)
SELECT
    COUNT(*) AS total_candidates,
    COUNT(*) FILTER (
        WHERE n_post_adopt >= 5
    ) AS previous_sample,
    COUNT(*) FILTER (
        WHERE adoption_ts <= TIMESTAMP '2026-03-31 23:59:59'
                             - INTERVAL 30 DAY
    ) AS eligible_30_days,
    COUNT(*) FILTER (
        WHERE adoption_ts <= TIMESTAMP '2026-03-31 23:59:59'
                             - INTERVAL 60 DAY
    ) AS eligible_60_days,
    COUNT(*) FILTER (
        WHERE adoption_ts <= TIMESTAMP '2026-03-31 23:59:59'
                             - INTERVAL 90 DAY
    ) AS eligible_90_days,
    COUNT(*) FILTER (
        WHERE n_post_adopt = 0
    ) AS zero_post_prs,
    MIN(adoption_ts) AS earliest_adoption,
    MAX(adoption_ts) AS latest_adoption
FROM candidates
""", [str(SAMPLE)]).df()

print(result.to_string(index=False))

con.close()
