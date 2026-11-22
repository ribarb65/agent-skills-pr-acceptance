from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
OUTPUT = ROOT / "data" / "cleaned_matched_pairs.csv"

pairs = pd.read_csv(PROCESSED / "rq1_matched_pairs.csv")
rq1 = pd.read_csv(PROCESSED / "rq1_paired_results.csv")
rq2 = pd.read_csv(PROCESSED / "rq2_heterogeneity_pairs.csv")

assert len(pairs) == 424
assert len(rq1) == 184
assert len(rq2) == 184

for table in [pairs, rq1, rq2]:
    assert table["pair_id"].is_unique

assert set(rq1["pair_id"]).issubset(set(pairs["pair_id"]))
assert set(rq2["pair_id"]) == set(rq1["pair_id"])

cleaned = pairs.merge(
    rq1,
    on="pair_id",
    how="left",
    validate="one_to_one"
)

rq2_columns = [
    "pair_id",
    "did",
    "reuse_group",
    "compat_group",
    "alignment_group"
]

cleaned = cleaned.merge(
    rq2[rq2_columns].rename(columns={"did": "rq2_did"}),
    on="pair_id",
    how="left",
    validate="one_to_one"
)

cleaned["complete_case"] = cleaned["did"].notna()

included = cleaned.loc[cleaned["complete_case"]].copy()

assert len(cleaned) == 424
assert len(included) == 184
assert cleaned["pair_id"].is_unique

assert np.allclose(
    included["did"],
    included["rq2_did"]
)

reconstructed_did = (
    included["treated_after"]
    - included["treated_before"]
    - included["control_after"]
    + included["control_before"]
)

assert np.allclose(
    reconstructed_did,
    included["did"]
)

assert included[
    ["reuse_group", "compat_group", "alignment_group"]
].notna().all().all()

cleaned = cleaned.drop(columns=["rq2_did"])

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

cleaned.to_csv(
    OUTPUT,
    index=False,
    na_rep=""
)

verification = pd.read_csv(OUTPUT)

assert len(verification) == 424
assert verification["complete_case"].sum() == 184

print("CLEANED DATASET VALIDATION: PASSED")
print("Total matched pairs:", len(verification))
print("Complete analysis pairs:", verification["complete_case"].sum())
print("Excluded from complete-case analysis:", (~verification["complete_case"]).sum())
print("Missing outcomes preserved as blank: YES")
print("RQ1 and RQ2 estimates consistent: YES")
print("File:", OUTPUT)
