# C09 — shared wrong result, Pair B

## Observed results and vote

C09 asks for revenue excluding VAT from **all orders** by customers exactly 25
on the fixed reference date **2026-09-26**. The real, saved TD1 traces
(`../../TD1/kit-td1/traces-td1.csv`, cells
`openrouter:cohere/north-mini-code:free:C09` and
`groq:qwen/qwen3.8-27b:C09`) mark both answers **0 cents** as `incorrect`.
The independent `../../TD1/kit-td1/reference-td1.csv` states **487980 cents**.
These are recorded observations; the clause diagnosis below explains them.

| Model | C09 value (cents) | Fixed 2-of-3 | Full 3-of-5 |
|---|---:|:---:|:---:|
| GPT-OSS 120B | 487980 | yes | yes |
| North Mini Code | 0 | yes | yes |
| Qwen 3.8 27B | 0 | yes | yes |
| GPT-OSS 20B | 487980 | no | yes |
| Dots 3 Note Preview | 548920 | no | yes |

With **k=2, n=3**, North and Qwen's zero wins: **wrong consensus 0**.
With **k=3, n=5**, the vote splits 2–2–1: **abstain**, maximum two votes.
The full twenty-question vote is in `../pair-a/vote-comparison.csv`.

## Why the two complete SQL queries fail

The complete, unedited SQL statements returned in the TD1 trace are stored in
[`c09-north-as-returned.sql`](c09-north-as-returned.sql) and
[`c09-qwen-as-returned.sql`](c09-qwen-as-returned.sql).
Both execute successfully on the shop database and return zero, as recorded in
[`c09-results.txt`](c09-results.txt).

- **North:** Its age expression starts with
  `CAST(SUBSTR(c.birth_date, 1, 4) AS INTEGER)` (the **birth year**) and
  subtracts either zero or one. It compares that expression to 25. It should
  start with the reference year **2026**. For a customer born in 2001, its
  expression is around 2000/2001, never 25; the valid customers are excluded.
- **Qwen:** It uses `o.date` (the order date) to test age, although C09 asks
  for age on the fixed reference date. Its final two tests also require the
  order's month and day to be simultaneously **at least** the birth month/day
  and **less than** the month/day of `birth_date + 26 years`. For the eligible
  customers shown below, adding 26 years preserves the month/day. Those
  inequalities cannot both hold, so their orders are excluded. The query
  implements neither the fixed-date age test nor a working age-at-order test.

The correct cohort is birth dates **after 2000-09-26 and on or before
2001-09-26**. The independent check in
[`c09-independent-check.sql`](c09-independent-check.sql) computes completed
age from the reference year and whether the birthday has occurred. A separate
TD1 boundary-based reference query is in
`../../TD1/yehor-nalyvaiko/references/C09.sql`; both yield 487980 cents.

## Executed delta and independent check

[`c09-delta.sql`](c09-delta.sql) reproduces each faulty `WHERE` predicate
on every order line, selects customers in the correct age cohort, and groups
their omitted revenue by `customer_id`.
Its executed result is [`c09-delta.csv`](c09-delta.csv): six customers, with
**487980 cents** of reference revenue, all **487980 cents** missed by North
and all **487980 cents** missed by Qwen. This accounts for the exact
**487980 − 0 = 487980 cent** gap for each query. The independent check is the
separate age calculation and direct execution of both stored model queries.

Replay from the repository root, without model or network calls:

```bash
DB=TD1/kit-td1/data/boutique.sqlite
sqlite3 -readonly "$DB" < TD2/pair-b/c09-north-as-returned.sql
sqlite3 -readonly "$DB" < TD2/pair-b/c09-qwen-as-returned.sql
sqlite3 -readonly "$DB" < TD2/pair-b/c09-independent-check.sql
sqlite3 -readonly -csv "$DB" < TD2/pair-b/c09-delta.sql
```

The `c09-delta.csv` file adds column names to that last command's six rows.
The zero agreement is a **real batch result**, not the workshop's synthetic
`DEMO-VOTE` or historical `DEMO-SQL-C11` example. These observations cover
this database and this run; they do not establish a general error rate.
