# TD 1 — Yehor Nalyvaiko: questions C09 and C10

Pack `2026-10-18-students-1`, database `boutique.sqlite` sha256 `0077e235…3398fec2` (identical to `manifest.json`).
Environment: Python 3.14.6, sqlite3 3.53.2, Windows 11. Run on 21 October 2026.

## References (step 1)

| Case | Value (cents) | Query | Independent check |
|---|---|---|---|
| C09 | 487980 | `references/C09.sql`: born after 2000-09-26 and on or before 2001-09-26 | `references/C09-check.sql`: year difference minus 1 if the birthday (month-day) is not reached on 2026-09-26 |
| C10 | 558980 | `references/C10.sql`: date(o.date, '-26 years') < birth_date <= date(o.date, '-25 years') | `references/C10-check.sql`: same completed-age formula with the date of each order |

Convention: completed age computed from month and day, never from the year difference alone.
Each value was confirmed by the second query and by a separate Python computation. No customer is born on 29 February.
`references/reference-C09-C10.csv` holds the two rows in the format of `reference-td1.csv`.

**AI assistance (declared):** the reference queries were written with the help of Claude (Anthropic) and checked as above.

## Model calls (step 2)

Five required models × C09, C10 = 10 initial calls (6 Groq, 4 OpenRouter), 1 attempt each, no retry.
Same prompt fingerprint for all models on a question: C09 `8a183ea0b704…`, C10 `bf06c7f2b73e…`.

```powershell
python skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b groq:openai/gpt-oss-20b groq:qwen/qwen3.8-27b openrouter:cohere/north-mini-code:free openrouter:dots-studio/dots-3-note-preview:free --cases C09,C10 --state state-yehor.jsonl --out traces-yehor.csv
```

Raw traces: `traces/traces-yehor.csv` (CSV export) and `traces/state-yehor.jsonl` (state). All rows are real calls.

## Results and causes (step 3)

| Model | C09 | C10 |
|---|---|---|
| groq:openai/gpt-oss-120b | correct | correct |
| groq:openai/gpt-oss-20b | correct | correct |
| openrouter:cohere/north-mini-code:free | incorrect (0) | incorrect (548920) |
| groq:qwen/qwen3.8-27b | incorrect (0) | sql_rejected |
| openrouter:dots-studio/dots-3-note-preview:free | incorrect (548920) | incorrect (119410) |

One cause per failed cell, read from the returned SQL: `comparison-yehor-C09-C10.csv` (format of `model-question-comparison-en.csv`).
Main cause: the completed-age convention (year difference without month-day). 548920 is exactly the value of the
year-only query on the base, reached by two different models on two different questions.
qwen C10 is an output-format failure (SQL inside a markdown fence, HTTP 200), not an access failure.

Missing measurements stay empty: no native cost on Groq rows (missing, not zero); OpenRouter `:free` rows report 0.
