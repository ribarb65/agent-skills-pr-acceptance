
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "interim"

con = duckdb.connect()

adoption = DATA / "repo_adoption.parquet"
sample = DATA / "phase0_usable_adopters.parquet"

for file in (adoption, sample):
    if not file.exists():
        raise FileNotFoundError(file)

print("Adoption date status")

print(con.execute("""
    SELECT date_status, COUNT(*) AS repositories
    FROM read_parquet(?)
    GROUP BY date_status
    ORDER BY repositories DESC
""", [str(adoption)]).df().to_string(index=False))

print("\nAIDev v5 sample")

print(con.execute("""
    SELECT
        COUNT(*) AS candidates,
        COUNT(*) FILTER (
            WHERE date_status = 'complete'
        ) AS complete_dates,
        COUNT(*) FILTER (
            WHERE n_post_adopt >= 5
        ) AS enough_post_prs,
        COUNT(*) FILTER (
            WHERE date_status = 'complete'
              AND n_post_adopt >= 5
        ) AS both_conditions,
        COUNT(*) FILTER (
            WHERE date_status = 'partial'
        ) AS partial_dates
    FROM read_parquet(?)
    WHERE scope = 'v5/all'
""", [str(sample)]).df().to_string(index=False))

con.close()
