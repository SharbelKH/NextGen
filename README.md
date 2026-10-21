# NextGen — Trustworthy Generative AI (ESILV A4 DIA, Next-Generation AI)

Shared repository of the sub-group, from TD 1 (21 October 2026) to TD 3 (11 December 2026).
Course site (single reference): https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/index.html

| | |
|---|---|
| DIA / sub-group | _to complete_ |
| Members | _to complete (name — GitHub account — TD 1 role A–H)_ |
| Course pack | `2026-10-18-students-1` (student ZIP `esilv-student-2026-10-18.zip`, sha256 `e14ebfb4437ca6a5…`) |
| Database | `kit-td1/data/boutique.sqlite`, sha256 `0077e235…3398fec2`, identical to `kit-td1/data/manifest.json` |
| Models | `kit-td1/modeles-autorises.json` (selection of 14 October 2026) |

## Repository layout

| Path | Content |
|---|---|
| `kit-td1/` | the course kit: database, questions, skeleton, sandbox, model configuration, result templates |
| `reports/td1.md` … `td3.md` | session reports (one per TD) |
| per-member branches | e.g. `yehor/td1-C09-C10`: references and traces of one member, merged here by pull request |

## Environment

Python 3.10 or later, package `requests` (network checks only). API keys only as environment variables
`GROQ_API_KEY` and `OPENROUTER_API_KEY`, never in a file of this repository (see `.gitignore`).

## Replay the work (from a fresh clone)

```bash
cd kit-td1
python verify-data.py                 # database integrity: last object "ok": true
python check_access.py --no-network   # local checks only, no API call
python skeleton-multi-llm-en.py --replay traces-td1.jsonl   # re-run stored SQL offline (once traces are merged)
```

A new network run uses the free quotas of the operators' accounts; see `kit-td1/consigne-etudiante-en.md` §5.

## Hand-ins

Moodle entry per TD: repository URL, members, full commit hash of the session, link to `reports/tdN.md` at that commit.
Deadlines: 25 October, 22 November, 13 December 2026, 23:59 Paris time.
