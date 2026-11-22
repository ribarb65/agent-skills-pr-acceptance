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

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/00_phase0_feasibility.ipynb
```

| Step | Script | Outputs |
|---|---|---|
| Phase 0 — feasibility (schemas, adoption dates, funnel) | `notebooks/00_phase0_feasibility.ipynb` | `data/processed/phase0_funnel.csv`, `figures/phase0_*.png` |
| Course proposal | `report/build_proposal.py`, `report/docx_to_pdf.py` | `report/Project_Proposal.{docx,pdf}` |

## Repository layout

```
data/raw/        downloaded extracts (git-ignored, never modified)
data/interim/    intermediate tables (git-ignored)
data/processed/  small result tables
data/external/   hand-curated reference tables with sources
notebooks/       analysis notebooks, executed with outputs
figures/         generated figures
report/          proposal and paper sources
src/             reusable code
```

## Ethics and personal data

Only public data are used. No personally identifiable information is downloaded or stored: the extracts exclude
user logins, pull-request titles and bodies, and commit messages. GitSkills already replaces commit authors with
keyed one-way codes. Any data collected later through the GitHub API will pseudonymise human accounts at
collection time with a keyed one-way hash whose key never leaves the collecting machine.
