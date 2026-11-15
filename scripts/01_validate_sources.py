
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

EXPECTED = {
    "gitskills_artifacts_light.parquet": [
        "repo_full_name", "path", "filename",
        "location_class", "first_commit_at"
    ],
    "gitskills_repos.parquet": [
        "full_name", "is_fork", "created_at"
    ],
    "aidev_v5_all_pr.parquet": [
        "id", "agent", "state", "created_at",
        "merged_at", "repo_url"
    ],
    "aidev_v5_pop_pr.parquet": [
        "id", "agent", "state", "created_at",
        "merged_at", "repo_url"
    ]
}

con = duckdb.connect()

files = sorted(RAW.glob("*.parquet"))
print(f"Files found: {len(files)}/10")

for file in files:
    try:
        count = con.execute(
            "SELECT COUNT(*) FROM read_parquet(?)",
            [str(file)]
        ).fetchone()[0]

        columns = {
            row[0] for row in con.execute(
                "DESCRIBE SELECT * FROM read_parquet(?)",
                [str(file)]
            ).fetchall()
        }

        missing = set(EXPECTED.get(file.name, [])) - columns

        print(f"\n{file.name}")
        print(f"Rows: {count:,}")
        print(f"Columns: {len(columns)}")
        print(f"Schema: {'OK' if not missing else sorted(missing)}")

    except Exception as e:
        print(f"{file.name}: ERROR - {e}")

CHECKS = {
    "aidev_v5_all_pr.parquet": [
        "id", "agent", "repo_url", "created_at"
    ],
    "gitskills_artifacts_light.parquet": [
        "repo_full_name", "filename", "path",
        "first_commit_at"
    ]
}

for name, columns in CHECKS.items():
    path = RAW / name

    if not path.exists():
        continue

    print(f"\nMissing values: {name}")

    for column in columns:
        result = con.execute(
            f"SELECT COUNT(*) FILTER (WHERE {column} IS NULL) "
            "FROM read_parquet(?)",
            [str(path)]
        ).fetchone()[0]

        print(f"{column}: {result:,}")

con.close()
