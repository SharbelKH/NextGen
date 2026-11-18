# TD 1 — Comparing five models on revenue questions

DIA1, subgroup 1. Session: 21 October 2026. Consolidated on 30 October 2026.

## What we did

We split the twenty questions between the group members and tested the five
models from the course kit. Each model received the question, schema and
common conventions. The runner executed the SQL in the read-only sandbox
and compared the amount with the reference.

We started by writing reference queries. During the session, the teacher
provided the reference values and asked us to focus on the model runs. The
comparison uses those values in [reference-td1.csv](../kit-td1/reference-td1.csv).
Some reference SQL is saved there and in members' folders. We left the other
SQL fields empty rather than filling them with model answers. We do not claim
an independent group calculation for every reference.

## Evidence and results

- [Raw CSV](../kit-td1/traces-td1.csv): 108 attempts, including eight authentication failures.
- [Combined JSONL](../kit-td1/traces-td1.jsonl): the same 108 records, rebuilt from the source CSVs for offline use.
- [Source index](../kit-td1/trace-sources.csv): original file, record number and SHA-256 for every combined record.
- [Final comparison](../kit-td1/model-question-comparison-en.csv): 100 last-attempt results with explanations.
- [Five-model summary](../kit-td1/five-model-summary-en.csv): results by family and dated portfolio information.
- [Matrix view](td1-matrix.md), [exact prompts](../prompts-en.md) and [model configuration](../kit-td1/modeles-autorises.json).

| Model and route | Correct / 20 cells | Incorrect | SQL rejected | Final access errors |
|---|---:|---:|---:|---:|
| GPT-OSS 120B, Groq | 19/20 | 1 | 0 | 0 |
| GPT-OSS 20B, Groq | 18/20 | 2 | 0 | 0 |
| North Mini Code, OpenRouter | 13/20 | 7 | 0 | 0 |
| Qwen 3.8 27B, Groq | 13/20 | 5 | 2 | 0 |
| Dots 3 Note Preview, OpenRouter | 15/20 | 5 | 0 | 0 |

There are 78 correct answers, 20 incorrect answers and two rejected outputs.
No cell is unfinished. A rejected output is a failed cell, but it is different
from an executed query returning the wrong amount.

The summary uses four separate categories: period-only (6 questions), age-only
(5), product-list (4), and combined filters (5). Combined cases are counted
only in the combined category, so the category totals add up to twenty.

## What went wrong

All twenty executed wrong answers involved age questions, sometimes together
with other filters. For example:

- Qwen C15 requires the birthday to be both on or before 25 September and
  after 25 September. No row can match, so the result is zero.
- Qwen C16 and C17 use the wrong inclusivity at the birthday boundary.
- Dots C10 and C18 miss people who are still 25 before their 26th birthday.
- GPT-OSS 120B C19 selects just one birth date instead of a one-year window.
  The model with the most correct results still makes an age error.
- North Mini Code C17 builds month-year where it needs month-day.

Qwen C03 and C10 were rejected because the returned text began with an
unclosed markdown SQL fence. The sandbox reported `not_select`. Both calls
had HTTP 200, so these were output-format failures, not refused access. We
kept the rejection rather than editing the SQL and counting it as right.

Every non-correct final row has a cause in the comparison. The causes were
read from the saved SQL and errors; no extra model calls were made for this
analysis. Matching an amount does not prove that a query would also be
correct on a different database.

## Authentication and additions on 30 October

Sherbal Al khouri's first six OpenRouter calls for C15, C16 and C20 failed with HTTP 401
on 21 October. After replacing the key, he retried the six cells and received
answers. The runner's resume check was adjusted to allow an explicit retry
after a saved 401, while keeping the maximum of two attempts per cell.

When we combined the files, Dots C07 and C08 were missing. Sherbal Al khouri ran these
two cells on **30 October 2026**, after the original session and deadline.
Both first attempts failed authentication. After checking the corrected key,
both second attempts succeeded: C07 = 13970 cents and C08 = 605580 cents.

These are late additions, not session-day runs. The 21 October evidence covers
98 cells: 76 correct, 20 incorrect and two rejected. Adding the two correct
Dots results gives 100 cells. The comparison marks their date explicitly.
All eight authentication failures and original timestamps remain in the raw
traces. The account checks used while fixing keys are separate from these
model-call counts.

## Combining the files

The member files were preserved. The old shared C01/C02 CSV and JSONL were
copied byte-for-byte into [raw-c01-c02](../kit-td1/raw-c01-c02/) before their
shared output names were used for the combined evidence. The combined JSONL
is a CSV-to-JSONL conversion, not another set of calls. Original JSONL state
files remain in the member locations; Adam supplied his eight records as CSV.

The consolidation script checks all 100 expected cells, reference values,
prompt hashes, verdict/value agreement and the two-attempt limit. Each
question's fingerprint also matches the exact prompt generated by the saved
skeleton, schema and question text. Source line endings and a UTF-8 header
marker are normalised only in the combined files.

Regenerate the outputs from the repository root:

```bash
python3 tools/consolidate_td1.py
```

This reads saved files. It does not execute SQL or contact providers.

## Contributions

| Contribution | Evidence |
|---|---|
| Chaima: C01, C02 | `kit-td1/raw-c01-c02/` |
| Mariem: C03, C04 | `kit-td1/traces-mariem-*.csv` and matching state files |
| Valentina: C05, C06, C17 | `kit-td1/traces-valec-c05-c06-c17.csv` |
| Adam: C07, C08 for four models | `kit-td1/adam-nasri-work/` |
| Yehor: C09, C10 | `yehor-nalyvaiko/` |
| Oussama: C11, C12, C19 | `oussama-meziane/` |
| Pablo: C13, C14, C18 | `pablo-laxague/` |
| Sherbal Al khouri: C15, C16, C20; late Dots C07/C08; group consolidation | `sharbel-khoury/`, combined outputs and this report |

## Limits and next steps

This is one set of twenty questions on one small database, with different
operators and accounts. Dots C07/C08 were run nine days later. These results
do not establish a stable general ranking or measure repeatability.

Missing native costs and token measurements remain empty. A missing Groq
cost is not a measured zero. The model summary uses the supplied portfolio
dated 28 September, not current prices. Only GPT-OSS 120B has a documented
paid route in that snapshot. Unsupported paid-route prices from the previous
summary were replaced with N/A; free-route prices were not used as paid prices.

The period-only questions were easier than the age questions in this batch.
A routing rule could start with a cheaper model for simple period questions
and require extra checks for age logic. We need more evidence before treating
that as a production rule. TD 2 can test voting on these saved traces without
repeating the network calls. Agreement still needs checking against references.

Submit the final repository URL, full commit hash and report link at that
commit. This update must not be
described as the original 25 October submission.

## Assistance

Codex was used for assistance only and fixing errors.
