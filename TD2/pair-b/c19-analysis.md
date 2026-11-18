# C19 — shared wrong result, Pair B evidence (contributed by Pair A)

## Observed results and vote

C19 asks for the revenue excluding VAT, in euro cents, of **product d only**, for orders placed from
2026-09-01 00:00:00 (included) to 2026-10-01 00:00:00 (excluded), by customers **exactly 25 on the
reference date 2026-09-25**. The saved TD1 traces (`../../TD1/kit-td1/traces-td1.csv`, cells
`groq:openai/gpt-oss-120b:C19` and `openrouter:cohere/north-mini-code:free:C19`) mark both answers
**0 cents** as `incorrect`. The independent `../../TD1/kit-td1/reference-td1.csv` states **1990 cents**.

| Model | C19 value (cents) | Fixed 2-of-3 | Full 3-of-5 |
|---|---:|:---:|:---:|
| GPT-OSS 120B | 0 | yes | yes |
| North Mini Code | 0 | yes | yes |
| Qwen 3.8 27B | 83580 | yes | yes |
| GPT-OSS 20B | 1990 | no | yes |
| Dots 3 Note Preview | 1990 | no | yes |

With **k=2, n=3**, the two zeros win: **wrong consensus 0**. With **k=3, n=5**, the vote splits
2–2–1 (0, 1990, 83580): **abstain**, maximum two votes. The twenty decisions are in
[`vote-comparison.csv`](../pair-a/vote-comparison.csv).

## Why the two SQL queries fail

The complete SQL statements returned in the TD1 trace are stored unedited in
[`c19-120b-as-returned.sql`](c19-120b-as-returned.sql) and
[`c19-north-as-returned.sql`](c19-north-as-returned.sql). Both run without error on the shop database
and return 0 ([`c19-results.txt`](c19-results.txt)). The product filter (`o.product_id = 'd'`) and
the period filter are correct in both; only the **age predicate** is wrong.

- **GPT-OSS 120B:** `c.birth_date = date('2026-09-25', '-25 years')`, that is
  `birth_date = '2001-09-25'`. It keeps customers whose **25th birthday falls on the reference date**,
  not every customer aged 25. "Exactly 25" means completed age 25: born after 2000-09-25 and on or
  before 2001-09-25, a one-year window. One customer is born on that very day (C001), but C001 has
  no product d order in September, so the sum is 0.
- **North Mini Code:** it computes an age as
  `(strftime('%Y-%m-%d', '2026-09-25') - strftime('%Y-%m-%d', c.birth_date)) / 365`.
  SQLite subtracts two date strings by converting each to its leading number, the year:
  `'2026-09-25' - '2001-09-24'` = 2026 − 2001 = **25 years, not 25 × 365 days**. Dividing by 365 in
  integer arithmetic gives **0**. The window then becomes `date('2026-09-25', '-0 years')` and
  `date('2026-09-25', '-1 years')`: customers born between 2025-09-25 (excluded) and 2026-09-25
  (included), i.e. babies. No customer is that young (the youngest is born 2006-08-15), so the
  query keeps nobody and returns 0.

The two errors are different: 120B narrows the cohort to one day, North shifts it to the wrong
year. They meet on the same value only because the empty sum is 0 (`COALESCE(SUM(…), 0)`).
A zero from an empty selection looks like a valid answer to the vote.

## Executed delta and independent check

The correct cohort, from the customer table, is six customers: C005 (2000-09-26), C007, C009, C008,
C002 (2001-09-24) and C001 (2001-09-25). [`c19-delta.sql`](c19-delta.sql) applies the product and
period filters, reproduces each model's age predicate on every order line, keeps the reference
cohort and groups the omitted revenue by `customer_id`. Its executed result
[`c19-delta.csv`](c19-delta.csv) has one row:

| customer_id | birth_date | reference revenue | missed by 120B | missed by North |
|---|---|---:|---:|---:|
| C002 | 2001-09-24 | 1990 | 1990 | 1990 |

Only one order line of product d in September comes from the cohort: C002, one unit at 1990 cents
on 2026-09-07. C002 turned 25 on 2026-09-24, **one day before the reference date**. 120B misses it
because its test keeps only 2001-09-25; North misses it because its window is in 2025–2026. The
delta sums to **1990 cents** for each model, exactly 1990 − 0. It also equals the reference value,
an independent check of `reference-td1.csv` (the TD1 reference was computed separately, see
`../../TD1/oussama-meziane/notes-oussama.md`).

Replay from the repository root (read-only on `TD1/kit-td1/data/boutique.sqlite`, rewrites
`c19-results.txt` and `c19-delta.csv`):

    python3 -B TD2/pair-b/c19-replay.py

## Limits

This explains C19 in this saved batch and this database. The question is a boundary case by
design: the only paying customer of the cohort sits one day from the reference date, so any age
rule that is off by a day or by a year gives 0. It does not measure a general error rate of
either model.
