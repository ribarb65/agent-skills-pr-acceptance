
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data/interim/phase0_usable_adopters.parquet"

con = duckdb.connect()

result = con.execute("""
WITH candidates AS (
    SELECT DISTINCT
        repo,
        adoption_ts
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
      AND date_status = 'complete'
      AND n_pre_adopt >= 5
),
treated AS (
    SELECT *
    FROM candidates
    WHERE adoption_ts <= TIMESTAMP '2026-03-31 23:59:59'
                         - INTERVAL 60 DAY
),
control_counts AS (
    SELECT
        t.repo,
        COUNT(c.repo) AS potential_controls
    FROM treated t
    LEFT JOIN candidates c
        ON c.repo <> t.repo
       AND c.adoption_ts > t.adoption_ts + INTERVAL 60 DAY
    GROUP BY t.repo
)
SELECT
    COUNT(*) AS treated_repositories,
    COUNT(*) FILTER (
        WHERE potential_controls = 0
    ) AS no_potential_controls,
    MIN(potential_controls) AS min_controls,
    ROUND(AVG(potential_controls), 2) AS avg_controls,
    MAX(potential_controls) AS max_controls
FROM control_counts
""", [str(SAMPLE)]).df()

print(result.to_string(index=False))

con.close()