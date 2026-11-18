
# TD2 — Pair C: Routing Rule and Simulation Report

## 1. Objective

The goal is to build a routing policy that selects a suitable
AI model based on TD1 accuracy, cost, availability and the risk
of an incorrect answer.

Our policy covers eight question families and uses the five
models tested in TD1. The detailed accuracy results and
routing rules are in `TD2/routing-policy.md`.

## 2. Simulator Results: Before and After

We ran the seven supplied scenarios before adaptation and
compared them with the results after applying our policy.

| Scenario | Before adaptation | After adaptation |
|---|---|---|
| Simple | Run: small-free | Run: GPT-20B |
| Complex | Run: senior-subscription | Run: GPT-120B |
| Deferrable | Defer: 60 min | Defer: GPT-120B, 60 min |
| Urgent | Run: senior-api (€0.30) | Abstain |
| Budget exhausted | Abstain | Abstain |
| High impact | Run: senior-subscription | Run: GPT-120B + reference |
| Unknown capability | Abstain | Abstain |

### Main observations

- Simple F1 questions use GPT-20B, which scored 6/6 in TD1
  (C01, C04, C05, C06, C07, C20).
- F2 questions use GPT-120B, which scored 4/4 in TD1
  (C02, C08, C09, C11).
- The deferrable request waits 60 minutes for a quota refill.
- The urgent request now abstains because no eligible model
  is available before the deadline.
- High-impact payouts require a deterministic reference
  check or human review.
- Unknown families lead to abstention rather than guessing.

## 3. Priority: Subscription vs Free Quota Refill

In the original `choose` function, an immediately available
subscription resource (`cash == 0`, `allocation > 0`) is
selected before waiting for a free resource whose quota is
exhausted (`cash == 0`, `allocation == 0`).

This makes sense because the subscription has available
capacity and no additional cash cost for the request.
Running immediately also avoids delays and the risk of
missing the deadline.

However, we should reverse this priority when the request
is not urgent, its deadline allows waiting until the free
quota refills, and we want to preserve limited subscription
capacity for more urgent or important requests.

For example, a low-risk internal dashboard request could
wait for a free model instead of consuming subscription
capacity needed for a high-impact request.

## 4. Verification and Limitations

Our policy uses:
- No additional check for low-risk internal requests when
  the selected model achieved 100% accuracy in TD1.
- A 2-of-3 quorum for customer-facing figures.
- A deterministic reference or human review for payouts.

The simulator selects the required verification method but
does not execute the verification itself.

TD1 contains only 20 questions. These results support
a batch-specific routing decision, not a permanent ranking
or a guarantee of future accuracy.

The seven simulator scenarios demonstrate routing behavior
but do not prove that every possible request is handled
correctly. Additional family-level tests are useful.

## 5. Conclusion

The adapted simulator replaces generic resources with
models selected using TD1 evidence.

It prioritizes low-cost eligible models, adjusts verification
to the risk of errors, and can run, defer or abstain depending
on availability and deadlines.

The main trade-off is between immediate execution,
resource consumption and reliability.

---

## Pair A: the k-of-n vote and C19 (Yehor Nalyvaiko, Oussama Meziane, Adam Nasri)

**Vote.** `vote_k_sur_n` ([code](../pair-a/skeleton-multi-llm-en.py)) checks that `k` is a strict
majority (`n // 2 < k <= n`), refuses a duplicate `provider:model`, counts only executed values, and
returns a value only if it reaches `k` votes; otherwise it abstains. Errors and rejected SQL stay in
`n` without a vote. The reference is compared only after the decision. 13 contract tests pass
([output](../pair-a/out-tests.txt)); the four synthetic workshop cases give the expected results.

**Declared quorums on the twenty TD1 questions** (last attempt of each cell,
[full table](../pair-a/vote-comparison.md)):

| | correct consensus | wrong consensus | abstentions |
|---|---:|---:|---:|
| 2-of-3 panel (120B, North, Qwen; k=2) | 16 | **2** (C09, C19) | 2 (C10, C17) |
| 3-of-5 quorum (all five models; k=3) | 16 | **0** | 4 (C02, C09, C10, C19) |

The decision changes on four questions. C09 and C19: the two wrong zeros win in the panel, the
quorum abstains. C17: the panel splits three ways, the quorum reaches 258180 (correct). C02: the
panel is correct, but in the quorum 20B and Dots agree on a wrong 0 and block the majority. The
larger quorum removes the wrong decisions at the cost of two more abstentions.

**C19, shared wrong value 0** ([analysis](../pair-a/c19-analysis.md)). Reference **1990 cents**.
GPT-OSS 120B keeps only customers born on 2001-09-25 (`birth_date = date('2026-09-25', '-25 years')`),
whose 25th birthday is the reference date, instead of the one-year cohort born after 2000-09-25
and on or before 2001-09-25. North Mini Code subtracts two date strings: SQLite reads only the years,
so the "age in days" is 25, divided by 365 gives 0, and its window falls in 2025–2026, where no
customer is born. The [executed delta](../pair-a/c19-delta.csv) has a single line: C002, born
2001-09-24, one product d at 1990 cents on 2026-09-07, missed by both models; 1990 − 0 = 1990.
The two errors are different but both produce an empty selection, and the empty sum is 0.

**Limits.** 20 questions, one run per model: these counts describe this batch, not a general error
rate, and a quorum does not guarantee a correct answer.

---

## Pair B — Shared Wrong SQL Result (C09)

**Contributor:** Sherbal Al khouri

This is an in-progress group report. Pair B's C09 contribution is recorded below;
other members' sections and the final group review are still pending. The
workshop uses saved TD1 traces; no new model calls were made for this section.

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
[the analysis notebook](../pair-b/c02-analysis.ipynb), and C19's SQL diagnosis is in
[Pair A's analysis](../pair-a/c19-analysis.md). The group should integrate these contributions and routing
results before the TD2 hand-in.
