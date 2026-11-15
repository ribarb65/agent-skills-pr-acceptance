
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
        n_post_adopt,
        CASE
            WHEN adoption_ts > TIMESTAMP '2026-03-31 23:59:59'
                THEN 'After AIDev cutoff'
            WHEN adoption_ts > TIMESTAMP '2026-03-31 23:59:59' - INTERVAL 30 DAY
                THEN 'Less than 30 days'
            WHEN adoption_ts > TIMESTAMP '2026-03-31 23:59:59' - INTERVAL 60 DAY
                THEN '30 to 59 days'
            ELSE '60 days or more'
        END AS observation_group
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
      AND date_status = 'complete'
      AND n_pre_adopt >= 5
)
SELECT
    observation_group,
    COUNT(*) AS repositories,
    COUNT(*) FILTER (WHERE n_post_adopt = 0) AS zero_post_prs,
    COUNT(*) FILTER (WHERE n_post_adopt >= 5) AS five_or_more_post_prs,
    MIN(adoption_ts) AS earliest_adoption,
    MAX(adoption_ts) AS latest_adoption
FROM candidates
GROUP BY observation_group
ORDER BY
    CASE observation_group
        WHEN '60 days or more' THEN 1
        WHEN '30 to 59 days' THEN 2
        WHEN 'Less than 30 days' THEN 3
        ELSE 4
    END
""", [str(SAMPLE)]).df()

print(result.to_string(index=False))

con.close()
