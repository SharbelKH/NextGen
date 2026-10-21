# Prompts used in TD 1

Same prompt for the five models and the twenty questions, taken unchanged from
`kit-td1/skeleton-multi-llm-en.py` (`SYSTEM_PROMPT`, `USER_PROMPT_TEMPLATE`, pack 2026-10-18-students-1).
No variant was used. `{schema}` is the content of `kit-td1/schema.sql`, `{question}` the text of the case
in `kit-td1/questions-td1.json`. The fingerprint written in each trace line (`prompt_sha256`) is
`sha256(system + newline + user)`, so all models get the same fingerprint for a given question.

## System message

```text
You write SQLite queries for a small e-commerce database. Reply with exactly one SQLite SELECT statement and nothing else: no explanation, no comments, no markdown other than an optional ```sql fence.
```

## User template

```text
Schema (SQLite):
{schema}

Conventions (binding):
- product.price is the unit price in euro cents, excluding VAT (an integer). Revenue excluding VAT is SUM(quantity_product * price), an integer number of cents.
- orders holds order lines: one row per (order_id, product_id). All lines of an order share the same customer_id and the same date.
- orders.date and customers.insert_date are UTC timestamps stored as text 'YYYY-MM-DD HH:MM:SS'. customers.birth_date is a date stored as text 'YYYY-MM-DD'. Compare them as text or with SQLite date functions.
- A period "from S to E" is closed on the left and open on the right: date >= S AND date < E.
- A customer's age on a day D is the number of completed years: someone born on B is N years old on D when the N-th anniversary of B is on or before D and the (N+1)-th anniversary is after D. "Exactly 25 years old" means completed age 25 on that day, computed from month and day, never from the year difference alone.
- Unless the question says "at the time of the order", ages are computed on the reference date given in the question.
- The query must return exactly one row and one column named revenue_cents. When no order line matches, return 0 (use COALESCE), not NULL.
- Use only the tables above. One SELECT statement, nothing else.

Question: {question}
```

Model parameters (temperature 0, output cap, timeout) are read from `kit-td1/modeles-autorises.json`.
