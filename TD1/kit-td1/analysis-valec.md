# Analysis of C05, C06 and C17

All five models returned the correct reference values for C05 and C06. For C17, GPT-OSS 120B, GPT-OSS 20B and Dots returned the correct value of 258180 cents.

## C17 — Cohere North Mini Code

Observed result: 197080 cents. Reference: 258180 cents.

The SQL constructs a month-year string from the birth date and compares it with the month-day string `09-25`. This incorrectly determines whether the customer's birthday has occurred on the reference date.

The product filter, order period and revenue calculation are correct. The identified defect is in the age calculation.

## C17 — Qwen

Observed result: 248490 cents. Reference: 258180 cents.

The age filter excludes customers born on 25 September 2001, who turn 25 on the reference date, and includes customers born on 25 September 2000, who turn 26 that day.

The correct birth-date interval is greater than `2000-09-25` and less than or equal to `2001-09-25`.

## Evidence and scope

Evidence: `traces-valec-c05-c06-c17.csv` and `state-valec-c05-c06-c17.jsonl`.

All 15 recorded calls returned HTTP 200. There were no retries in this batch. The SQL defects were identified by inspecting the saved queries; no additional diagnostic queries were executed to quantify the affected customer contributions.

These findings concern three questions in this batch and do not establish a general ranking of the models.

AI assistance was used to prepare the reference SQL, execution scripts and this analysis. Reference query results were executed locally and matched the instructor's published values.