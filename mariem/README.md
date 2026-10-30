# Mariem — TD 1: C03 and C04

`queries.py` contains my reference SQL queries for C03 and C04. It checks the calculated answers against the shared boutique database.

This file is a copy of `../kit-td1/solve_c03_c04.py`, which remains unchanged in the group repository.

My recorded reference answers are:

- **C03:** 936350 cents (products a, b and c, orders from 1 January to 1 July 2026).
- **C04:** 2826250 cents (orders from 1 January to 1 October 2026).

These are the reference values used in my saved model tests.

## Model runs

I tested the five required models on C03 and C04 on **21 October 2026**, using the TD 1 kit. The uploaded trace files contain 10 recorded model results (one per model and question). I have not run any additional model calls to prepare this README.

The five models were Groq GPT-OSS 120B, Groq GPT-OSS 20B, OpenRouter North Mini Code (Cohere), Groq Qwen, and OpenRouter Dots.

The exact terminal commands used for the original runs are not established by the saved trace files, so I have not reconstructed them as if they were recorded commands.

## Results

| Model | C03 | C04 | Correct |
|---|---|---|---|
| Groq GPT-OSS 120B | correct | correct | 2/2 |
| Groq GPT-OSS 20B | correct | correct | 2/2 |
| OpenRouter North Mini Code | correct | correct | 2/2 |
| Groq Qwen | SQL rejected | correct | 1/2 |
| OpenRouter Dots | correct | correct | 2/2 |

There were **9 correct recorded results out of 10**. This only covers my two questions and does not establish an overall ranking of the models.

Qwen's C03 answer was rejected by the SQL validator (`sql_rejected`). Its response started with a Markdown SQL code fence (` ```sql `), rather than a plain SQL statement. No executed numeric result was recorded for that cell, so this is a **format/validation failure**, not evidence that the SQL arithmetic itself was incorrect. Qwen answered C04 correctly.

## Saved evidence

- `queries.py`: my reference-answer script for C03 and C04, copied from `../kit-td1/solve_c03_c04.py`.
- `traces-C03-C04.csv`: consolidated traces from the five original `traces-mariem-*.csv` files, covering 10 recorded cells.
- `state-C03-C04.jsonl`: consolidated saved state from the five original `state-mariem-*.jsonl` files.
- `comparison-mariem-C03-C04.csv`: 10 model-question results in the same column layout as Sharbel's comparison file.

The original per-model state and trace files remain in `kit-td1`; the consolidated files are additional copies for organization. Blank cost values should **not** be interpreted as zero cost.

The `queries.py` script uses the relative database path `data/boutique.sqlite`. To execute it correctly, run it from the `kit-td1` directory:

```bash
python ../mariem/queries.py
```

The group is responsible for consolidating all members' contributions into the final TD 1 deliverables.

## AI assistance

I used ChatGPT to organize the existing trace and state files, prepare the comparison file, interpret the saved verdicts, and draft this README in a format similar to a teammate's. ChatGPT did not make new model calls or change the original saved results.
