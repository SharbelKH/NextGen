# NextGen — Trustworthy Generative AI (ESILV A4 DIA, Next-Generation AI)

Shared repository of the sub-group, from TD 1 (21 October 2026) to TD 3 (11 December 2026).
Course site (single reference): https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/index.html

| | |
|---|---|
| DIA / sub-group | **DIA1 — subgroup 1** (instructor: Didier Parisot) |
| Members / contributions | Chaima, Mariem, Valentina, Adam, Yehor, Oussama, Pablo and Sherbal Al khouri. See the [TD 1 contribution table](reports/td1.md#contributions). |
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

## TD 1 results

The [session report](reports/td1.md) links the full submission. The combined
files contain 108 attempts and 100 final cells: 78 correct, 20 incorrect and
two SQL-format rejections.

- [Raw CSV](kit-td1/traces-td1.csv) and [combined JSONL](kit-td1/traces-td1.jsonl)
- [Source index](kit-td1/trace-sources.csv), linking each attempt to its original file
- [Final comparison](kit-td1/model-question-comparison-en.csv) and [matrix](reports/td1-matrix.md)
- [Five-model summary](kit-td1/five-model-summary-en.csv)
- [Reference values](kit-td1/reference-td1.csv) and [exact prompts](prompts-en.md)

Dots C07/C08 were added by Sherbal Al khouri on **30 October 2026**, after the original
session and deadline. They are marked as late additions. The session-day
evidence covers 98 cells. Original member files are retained; the old shared
C01/C02 files are preserved in `kit-td1/raw-c01-c02/`.

Regenerate the combined outputs offline from the repository root:

```bash
python3 tools/consolidate_td1.py
```

This does not execute SQL or call models. The combined JSONL is rebuilt from
the source CSVs, with one record per original attempt; it is not a new run.

## Replay the work (from a fresh clone)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install requests
cd kit-td1
python3 verify-data.py                 # database integrity: last object "ok": true
python3 check_access.py --no-network   # local checks only, no API call
python3 skeleton-multi-llm-en.py --replay traces-td1.jsonl --state traces-replay.jsonl --out traces-replay.csv
```

A new network run uses the free quotas of the operators' accounts; see `kit-td1/consigne-etudiante-en.md` §5.

Replay executes saved SQL locally and labels the output as replay. It is
optional; do not mix the replay outputs with the real-call evidence.

## Hand-ins

Moodle entry per TD: repository URL, members, full commit hash of the session, link to `reports/tdN.md` at that commit.
Deadlines: 25 October, 22 November, 13 December 2026, 23:59 Paris time.
