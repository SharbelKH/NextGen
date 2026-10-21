\# C11, C12 and C19: references and model results



Author: Oussama Meziane. Session: TD 1, 21 October 2026. Pack 2026-10-18-students-1.



\## References



| Case | Value (cents) | Method | Independent check |

|------|---------------|--------|-------------------|

| C11 | 446690 | SQL (`c11.sql`), completed age computed from year, month and day on 2026-12-01, all orders | Python on the CSV files (`check\_c11.py`): 6 customers aged exactly 25, same total |

| C12 | 1666490 | SQL (`c12.sql`), products a, b and c, all orders | Python on the CSV files (`check\_c12.py`), same total |

| C19 | 1990 | SQL (`c19.sql`), product d, orders from 2026-09-01 (included) to 2026-10-01 (excluded), customers exactly 25 on 2026-09-25 | Python on the CSV files (`check\_c19.py`): 6 customers aged 25, one matching order line, same total |



Age convention: a customer is exactly 25 on a reference date when born after that date minus 26 years and on or before that date minus 25 years. For C11 (2026-12-01) that means born after 2000-12-01 and on or before 2001-12-01. For C19 (2026-09-25), born after 2000-09-25 and on or before 2001-09-25.



\## Model run



Command: `skeleton-multi-llm-en.py --run --cases <case> --state state-oussama.jsonl --out traces-oussama.csv`, run for C11,C12 then for C19 in the same experiment.



15 real calls on 21 October 2026, one attempt per cell, no retry, no access error (HTTP 200 everywhere). All calls for a given question share the same prompt fingerprint, so differences come from the models, not from the wording.



| Model | C11 | C12 | C19 |

|-------|-----|-----|-----|

| groq:openai/gpt-oss-120b | correct | correct | incorrect (0) |

| groq:openai/gpt-oss-20b | incorrect (322160) | correct | correct |

| openrouter:cohere/north-mini-code:free | incorrect (0) | correct | incorrect (0) |

| groq:qwen/qwen3.8-27b | correct | correct | incorrect (83580) |

| openrouter:dots-studio/dots-3-note-preview:free | correct | correct | correct |



\## Failure analysis



\*\*gpt-oss-20b on C11 (322160).\*\* Filters `birth\_date > '2001-12-01' AND birth\_date <= '2006-12-01'`. That five-year window selects customers aged 20 to 24, not exactly 25. Valid SQL with a plausible amount, which makes the error hard to spot without a reference. Cause: age convention broken (wrong birth-date bounds).



\*\*cohere/north-mini-code on C11 (0).\*\* Filters `birth\_date > '2025-12-01' AND birth\_date <= '2026-11-25'`, so the 25 years were never subtracted, and adds an order-date filter for December 2026 that the question never asked for. Neither filter matches any row. Cause: age convention broken, plus an invented period filter.



\*\*gpt-oss-120b on C19 (0).\*\* Filters `birth\_date = date('2026-09-25', '-25 years')`, which keeps only customers born on 2001-09-25, that is whose 25th birthday falls on the reference date. No customer matches. Cause: age convention broken (equality instead of a one-year window). Product and period filters are correct.



\*\*cohere/north-mini-code on C19 (0).\*\* Subtracts two dates stored as text, which SQLite reduces to the year difference, then divides by 365, so the computed age is 0 and the value 25 never appears in the filter. It ends up selecting customers born in the last year, and there are none. Cause: broken age computation.



\*\*qwen3.8-27b on C19 (83580).\*\* Compares a year string (`'2026'`) with a full date (`'2026-09-25'`), a text comparison that is always true for years up to 2026. The filter therefore keeps every customer aged 25 or more, with no upper bound, and overcounts. Cause: age convention broken (lower bound only).



\## Observations and limits



\- Product-list question C12: 5/5 correct. Period and product filters were correct in every failing query.

\- Every failure on C11 and C19 comes from the age convention. None is invalid SQL or an access problem.

\- No model is correct on all three questions except dots-3-note-preview. gpt-oss-120b and qwen pass C11 but fail C19, while gpt-oss-20b fails C11 but passes C19, so success on one age question does not predict success on another.

\- One run per cell at temperature 0, on three questions only. This shows where these models can fail, not a general ranking.

