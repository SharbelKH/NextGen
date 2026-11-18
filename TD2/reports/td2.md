# TD2 session report — draft

This is an in-progress group report. Pair B's C09 contribution is recorded below;
other members' sections and the final group review are still pending. The
workshop uses saved TD1 traces; no new model calls were made for this section.

## Pair B: C09, shared wrong SQL result (Sherbal Al khouri)

**Question:** revenue excluding VAT in euro cents from all orders by customers
exactly 25 years old on 2026-09-26. The real TD1 trace cells
`openrouter:cohere/north-mini-code:free:C09` and
`groq:qwen/qwen3.8-27b:C09` each record `incorrect`, **0 cents**.
The independent `TD1/kit-td1/reference-td1.csv` records **487980 cents**.
The complete scan of all five models found C02, C09, and C19 as cases of
shared wrong values ([scan](../pair-b/find_shared_errors.py) and
[output](../pair-b/shared-errors-output.txt)).

**Declared quorums:** The fixed **2-of-3** panel (GPT-OSS 120B 487980,
North 0, Qwen 0) returns **0, wrong consensus**. The **3-of-5** panel adds
GPT-OSS 20B 487980 and Dots 548920; its 2–2–1 split returns **abstention**
(maximum two votes). [All twenty decisions](../pair-a/vote-comparison.csv).

**North Mini Code: full stored SQL** ([source](../pair-b/c09-north-as-returned.sql)):

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE
  -- Compute age on 2026-09-26
  (
    -- Age = year difference
    CAST(SUBSTR(c.birth_date, 1, 4) AS INTEGER) -
    CASE
      WHEN SUBSTR(c.birth_date, 6, 2) > '09' THEN 1
      WHEN SUBSTR(c.birth_date, 6, 2) = '09' AND SUBSTR(c.birth_date, 9, 2) > '26' THEN 1
      ELSE 0
    END
  ) = 25;
```

The `WHERE` expression takes the **birth year** (`SUBSTR(c.birth_date, 1, 4)`)
and subtracts zero or one, then asks whether the result equals 25. It should
start with **2026**, the reference year. Customers born around 2000–2001 are
thus excluded; the successful query returns zero.

**Qwen 3.8 27B: full stored SQL** ([source](../pair-b/c09-qwen-as-returned.sql)):

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE (strftime('%Y', o.date) - strftime('%Y', c.birth_date)) = 25
  AND (strftime('%m-%d', o.date) >= strftime('%m-%d', c.birth_date))
  AND (strftime('%m-%d', o.date) < strftime('%m-%d', date(c.birth_date, '+26 years')));
```

Qwen uses the **order date** (`o.date`) rather than the C09 reference date for
age. Further, for the relevant non-leap birthdays, `birth_date + 26 years`
has the same month/day as `birth_date`. The last two `WHERE` comparisons demand
that an order's month/day be both `>=` and `<` that same month/day. None of
the eligible customers' orders can pass these conditions.

**Independent check and exact delta:** Birth dates after 2000-09-26 and on or
before 2001-09-26 define age 25 on 2026-09-26. An independent completed-age
calculation in [c09-independent-check.sql](../pair-b/c09-independent-check.sql)
returns **487980 cents**. The executed [delta SELECT](../pair-b/c09-delta.sql)
lists each eligible `customer_id` and its order revenue in
[c09-delta.csv](../pair-b/c09-delta.csv): C001 135000, C002 25920,
C003 47900, C007 118740, C008 99090, C009 61330 cents. Both faulty
predicates miss all six customers' revenue; the omitted sums are **487980
cents** for each model, exactly **487980 − 0**. The stored queries were rerun
read-only on `TD1/kit-td1/data/boutique.sqlite` and again returned 0;
[replay commands and output](../pair-b/c09-analysis.md).

**Limits and next step:** This explains C09 in this saved batch and database;
it does not establish a general model error rate. Pair B's C02 work is in
[the analysis notebook](../pair-b/c02-analysis.ipynb), while C19's SQL diagnosis remains
with its owner. The group should integrate these contributions and routing
results before the TD2 hand-in.
