cat > README.md <<'EOF'
# Do Agent Skills Change the Acceptance of AI-Agent Pull Requests?

Replication repository for an MSR 2027 Mining Challenge study.

## Research Questions

**RQ1:** Does adding agent skills (`SKILL.md`) to a repository change the acceptance rate of AI-authored pull requests?

**RQ2:** Does this relationship vary with task–skill similarity, agent–skill compatibility, and skill provenance?

## Data Sources

| Dataset | Version | Source |
|---|---|---|
| GitSkills | July 2026 snapshot | `mvaccargiu/gitskills`, revision `ebab17454a7c236f8f26b183567f1a126f42e3f8` |
| AIDev | v5, PR cutoff March 31, 2026 | `hao-li/AIDev`, revision `b37f9fd1613cfec55886105bb76721918d015dc7` |
| Agent–skill compatibility | Curated reference | `data/external/agent_skill_locations.csv` |

## Environment Setup

Python 3.14 was used during development.

Run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt