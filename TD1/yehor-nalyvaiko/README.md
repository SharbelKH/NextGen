# C09, C10 — Yehor Nalyvaiko

Pack 2026-10-18-students-1 · Python 3.14 · Windows · 21/10/2026

## References
C09 = 487980, C10 = 558980 (same as the published values).
- `references/C09.sql`, `references/C10.sql`
- `references/C09-check.sql`, `references/C10-check.sql`: age computed another way, same result
- `references/reference-C09-C10.csv`

## Run
    python skeleton-multi-llm-en.py --run --models groq:openai/gpt-oss-120b groq:openai/gpt-oss-20b groq:qwen/qwen3.8-27b openrouter:cohere/north-mini-code:free openrouter:dots-studio/dots-3-note-preview:free --cases C09,C10 --state state-yehor.jsonl --out traces-yehor.csv

10 real calls, 1 attempt each. Traces: `traces/traces-yehor.csv`, `traces/state-yehor.jsonl`.

| Model | C09 | C10 |
|---|---|---|
| gpt-oss-120b | correct | correct |
| gpt-oss-20b | correct | correct |
| cohere north-mini-code | 0 | 548920 |
| qwen3.8-27b | 0 | rejected |
| dots-3-note-preview | 548920 | 119410 |

Causes: `comparison-yehor-C09-C10.csv`.

AI was used to help write the SQL and read the traces; all values were checked on the database. Details: [`coding-assistance.md`](coding-assistance.md).
