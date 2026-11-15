
from pathlib import Path
import duckdb

path = Path("data/raw/gitskills_artifacts_light.parquet")
con = duckdb.connect()

result = con.execute("""
SELECT
    location_class,
    COUNT(*) AS total,
    COUNT(first_commit_at) AS dated,
    COUNT(*) - COUNT(first_commit_at) AS missing,
    ROUND(100.0 * COUNT(first_commit_at) / COUNT(*), 2) AS coverage_pct,
    COUNT(DISTINCT LOWER(repo_full_name)) AS repositories
FROM read_parquet(?)
WHERE filename = 'SKILL.md'
GROUP BY location_class
ORDER BY total DESC
""", [str(path)]).df()

print(result.to_string(index=False))

summary = con.execute("""
SELECT
    COUNT(*) AS skills,
    COUNT(first_commit_at) AS dated,
    COUNT(DISTINCT LOWER(repo_full_name)) AS repositories
FROM read_parquet(?)
WHERE filename = 'SKILL.md'
AND location_class IN ('canonical', 'skills-dir')
""", [str(path)]).df()

print("\nStandard SKILL.md summary")
print(summary.to_string(index=False))

con.close()
