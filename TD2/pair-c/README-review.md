# Pair C — Cross-Pair Review of Pair A and Pair B

## 1. Objective

As part of TD2 — Next-Generation AI, Pair C reviewed the work completed by Pair A and Pair B.

The objective of this review is to:

- Evaluate the methodology and technical correctness of both investigations.
- Verify that their conclusions are supported by SQL queries and recorded results.
- Identify strengths, limitations, and possible improvements.
- Understand how their findings affect our own AI model routing and verification policy.

Both investigations demonstrate that different AI models can produce the same incorrect result, creating a misleading consensus.

---

## 2. Review of Pair A — C19

### 2.1. Summary of the Work

Pair A investigated question C19, which asks for the revenue excluding VAT, in euro cents, from product d orders placed between September 1 and September 30, 2026, by customers who were exactly 25 years old on September 25, 2026.

Two AI models produced the same incorrect result:

| Model | Returned result |
|---|---:|
| GPT-OSS 120B | 0 cents |
| North Mini Code | 0 cents |
| Correct reference | 1990 cents |

With a fixed 2-of-3 voting system, the two incorrect answers formed a wrong consensus of 0 cents.

With a 3-of-5 voting system, the answers were divided between 0, 1990, and 83580 cents, resulting in abstention.

### 2.2. Technical Verification

Pair A identified two different SQL errors.

**GPT-OSS 120B:** The model used an equality condition on the customer's birth date, selecting only customers born on September 25, 2001. However, being exactly 25 years old means having a birth date after September 25, 2000, and on or before September 25, 2001.

**North Mini Code:** The model incorrectly subtracted formatted date strings and divided the result by 365. SQLite interpreted the leading year values as numbers, causing an incorrect age calculation and excluding eligible customers.

The delta analysis identified customer C002, born on September 24, 2001, whose product d purchase contributed 1990 cents.

Both incorrect queries excluded this customer, explaining the entire difference between the model outputs and the reference.

### 2.3. Strengths

- The investigation clearly explains why two different SQL mistakes produced the same incorrect answer.
- The original SQL queries were preserved for reproducibility.
- A Python replay script reproduces the results.
- The delta analysis identifies the exact customer and revenue omitted by the models.
- The voting comparison demonstrates the limitations of majority-based verification.
- The report acknowledges that the results concern a specific dataset and do not establish general model reliability.

### 2.4. Suggestions for Improvement

**Automated boundary testing:** Add tests for customers born exactly on the age interval boundaries and immediately before or after them.

**Stronger independent verification:** The replay script compares its calculated result against a hardcoded reference value of 1990 cents. It would be useful to calculate the reference directly through an additional independent SQL query.

**Clearer voting summary:** Include a concise comparison of correct consensus, wrong consensus, and abstentions across all 20 TD1 questions.

### 2.5. Evaluation

Pair A's analysis is clear, technically consistent with the saved evidence, and reproducible using the provided scripts.

The main improvement would be stronger automated testing and independent validation.

The investigation demonstrates that agreement between AI models does not necessarily guarantee correctness.

---

## 3. Review of Pair B — C09

### 3.1. Summary of the Work

Pair B investigated question C09, which asks for the revenue excluding VAT from all orders made by customers who were exactly 25 years old on the fixed reference date of September 26, 2026.

Two models returned the same incorrect value:

| Model | Returned result |
|---|---:|
| North Mini Code | 0 cents |
| Qwen 3.8 27B | 0 cents |
| Correct reference | 487980 cents |

With a fixed 2-of-3 voting system, the two incorrect zeros formed a wrong consensus.

With a 3-of-5 voting system, the results were split 2–2–1, leading to abstention.

### 3.2. Technical Verification

Pair B correctly identified two different SQL errors.

**North Mini Code:** The query started its age calculation with the customer's birth year instead of the reference year 2026. For a customer born in 2001, the calculation produced a value close to 2001 instead of 25.

**Qwen:** The query used the order date rather than the fixed reference date to calculate age. It also contained contradictory month-and-day comparisons that excluded the eligible customers.

The correct birth-date interval was after September 26, 2000, and on or before September 26, 2001.

Pair B provided an independent SQL query and a delta analysis identifying six eligible customers.

The total omitted revenue was 487980 cents for both models, explaining the complete difference between their outputs and the reference result.

### 3.3. Strengths

- The original SQL queries were preserved without modification.
- Both incorrect outputs were reproduced using the shop database.
- The investigation identifies and explains two distinct age-calculation mistakes.
- An independent SQL query verifies the correct revenue.
- The delta analysis provides a detailed breakdown of the six eligible customers.
- The comparison between 2-of-3 and 3-of-5 voting demonstrates the risk of wrong consensus.
- The analysis clearly states that the findings apply to the saved batch rather than establishing a general model error rate.

### 3.4. Suggestions for Improvement

**Automated assertions:** Add tests confirming that the original model queries return 0 cents while the independent reference query returns 487980 cents.

**Boundary testing:** Test customers born on September 26, 2000, September 27, 2000, September 25, 2001, and September 26, 2001.

**Improved reproducibility:** Provide a Python-based replay option in addition to the SQLite command-line instructions to simplify execution across operating systems.

### 3.5. Evaluation

Pair B's investigation is technically consistent with the provided SQL queries and recorded results.

The independent reference calculation and per-customer delta analysis provide strong evidence supporting the conclusions.

The main suggested improvements concern automated testing and execution portability.

---

## 4. Comparison of Pair A and Pair B

| Criterion | Pair A — C19 | Pair B — C09 |
|---|---|---|
| Main objective | Investigate shared wrong revenue result | Investigate shared wrong revenue result |
| Incorrect model result | 0 cents | 0 cents |
| Correct reference | 1990 cents | 487980 cents |
| Models involved | GPT-OSS 120B and North | North and Qwen |
| Main error | Incorrect birth-date filtering | Incorrect age and reference-date calculations |
| Evidence | SQL queries, Python replay, delta | SQL queries, independent check, delta |
| 2-of-3 voting | Wrong consensus | Wrong consensus |
| 3-of-5 voting | Abstention | Abstention |
| Main improvement | Automated boundary and reference tests | Automated tests and reproducibility |

Both investigations successfully explain how different technical errors can produce the same incorrect result.

---

## 5. Implications for Pair C's Routing Policy

These investigations are particularly relevant to our own Pair C routing policy and Python simulator.

Our routing policy selects AI models based on TD1 accuracy, availability, and request risk. It also specifies verification requirements for internal dashboards, customer-facing figures, and payout amounts.

The findings from Pair A and Pair B highlight an important limitation:

**A 2-of-3 quorum can still produce an incorrect answer when two models agree on the same wrong result.**

Therefore, we recommend:

- Using independent deterministic checks for high-risk financial calculations whenever possible.
- Avoiding the assumption that majority agreement guarantees correctness.
- Considering abstention or human review when verification is insufficient.
- Adding tests for boundary conditions such as dates, ages, and numerical filters.
- Evaluating verification strategies based on both incorrect consensus and abstention rates.

These recommendations could strengthen the safety and reliability of our routing policy.

---

## 6. Overall Conclusion

Pair A and Pair B provided well-documented investigations supported by original SQL queries, execution results, and reference calculations.

Pair A demonstrated how incorrect birth-date filtering caused two models to return the same wrong answer for C19.

Pair B demonstrated how incorrect age calculations and reference-date conditions caused two models to return the same wrong answer for C09.

Both investigations highlight the limitations of relying exclusively on majority voting.

The analyses are consistent with the available evidence. We recommend additional automated tests, stronger independent verification, and clear documentation of verification limitations.

Overall, these findings provide useful evidence for improving Pair C's model-selection and verification strategy.

---

## 7. References

**Pair A:**
- [C19 analysis](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-b/c19-analysis.md)
- [C19 replay script](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-b/c19-replay.py)
- [Voting comparison](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-a/vote-comparison.csv)

**Pair B:**
- [C09 analysis](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-b/c09-analysis.md)
- [C09 independent SQL check](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-b/c09-independent-check.sql)
- [C09 delta results](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-b/c09-delta.csv)

**Pair C:**
- [Routing policy](https://github.com/SharbelKH/NextGen/blob/main/TD2/routing-policy.md)
- [Python routing simulator](https://github.com/SharbelKH/NextGen/blob/main/TD2/pair-c/atelier-routage.py)