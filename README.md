# Do agent skills change the acceptance of AI-agent pull requests?

Replication package for an MSR 2027 Mining Challenge study (GitSkills dataset).

- **RQ1** — Does adding agent skills (`SKILL.md` files) to a repository change the acceptance rate of pull
  requests authored by AI coding agents?
- **RQ2** — Does this effect vary with the match between the pull request's task and the skill, the compatibility
  between the agent and the skill's location, and the origin of the skill (copied or written locally)?

## Data sources (pinned versions)

| Dataset | Version used | Access |
|---|---|---|
| GitSkills | July 2026 collection (Zenodo DOI [10.5281/zenodo.21875637](https://doi.org/10.5281/zenodo.21875637)); Parquet mirror `mvaccargiu/gitskills` at commit `ebab17454a7c236f8f26b183567f1a126f42e3f8` | Hugging Face |
| AIDev | v5 (cutoff 2026-03-31), tag `v5`, commit `b37f9fd1613cfec55886105bb76721918d015dc7`; v3 (tag `v3`, commit `3ca0045773097b138b064550dfd6e72229f40bee`) for comparison only | Hugging Face `hao-li/AIDev` |
| Agent → skill locations | Hand-curated from official documentation and changelogs, one source per row | `data/external/agent_skill_locations.csv` |

Raw data are **not** stored in this repository: the notebooks download light column extracts into `data/raw/`
on first run (about 400 MB) and reuse them afterwards.

## Reproduce

The analysis uses Python, DuckDB, GitSkills, and AIDev v5.
Dataset revisions are pinned in the notebooks.

Run these commands from the repository root, in order:

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/00_phase0_feasibility.ipynb
    .venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/01_rq1_analysis.ipynb
    .venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/02_rq2_analysis.ipynb
    .venv/bin/python scripts/13_export_cleaned_matched_pairs.py

The initial execution requires Internet access to download the pinned
source datasets. Local Parquet extracts are cached for subsequent runs.
Full end-to-end execution in a fresh environment has not been independently verified.

## Cleaned Analytical Dataset

The cleaned analytical dataset is located at:

    data/cleaned_matched_pairs.csv

It contains 424 matched treated-control repository pairs.

Each row includes repository identifiers, adoption date, pre-adoption
PR activity, matching distance, and available outcome measurements.

The complete_case indicator identifies the 184 pairs with valid
before-and-after PR merge rates for both treated and control repositories.

The remaining 240 pairs retain missing outcome values as missing,
rather than replacing them with zero.

For complete pairs, the dataset also contains the RQ2 classifications
for task-skill alignment, documented agent-skill compatibility,
and observed skill-content reuse.

This file is a cleaned, aggregated analytical dataset, not the
complete individual pull-request corpus.

The export is generated and validated by:

    scripts/13_export_cleaned_matched_pairs.py

## Repository Structure

- data/cleaned_matched_pairs.csv: Cleaned analytical dataset
- data/processed/: Analysis results and statistical tables
- data/external/: Curated compatibility reference
- data/raw/: Downloaded source extracts, excluded from Git
- data/interim/: Intermediate datasets, excluded from Git
- notebooks/: Phase 0, RQ1, and RQ2 analyses
- scripts/: Validation and dataset export scripts
- figures/: Generated research figures
- report/: Project proposal and final report materials
- requirements.txt: Pinned Python dependencies

## Methodological Limitations

The main RQ1 analysis uses 184 complete pairs out of 424 matched pairs.

The study is observational and does not establish causal effects.

Historical skill content cannot always be reconstructed exactly.
Documented agent-skill compatibility does not prove actual skill usage.
Identical content hashes indicate observed reuse, not the direction
of copying or local authorship.

The historically restricted RQ2 sample contains 86 pairs.
Its findings should not automatically be generalized to all repositories.

## Data and Privacy

The analysis relies on public GitHub-related research datasets.
RQ2 processes pull-request titles, descriptions, and skill content.
Local intermediate extracts may contain identifying information
and are excluded from the Git repository.
