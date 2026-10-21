# Coding assistance — Yehor Nalyvaiko, TD 1

Assistant: Claude (Anthropic), used on my own computer. API keys were never shared with it;
the model calls of the experiment were run by me with the kit's skeleton.

| Step | Help requested | What it produced | How it was checked |
|---|---|---|---|
| References C09, C10 | Help translating the "completed age" convention into SQLite conditions for C09 (fixed date) and C10 (order date), and a way to run them on the database | `references/C09.sql`, `references/C10.sql` | Executed on `boutique.sqlite` (read-only); equal to the published reference values |
| Independent check | A second, different way of computing the age, to confirm the first query | `references/C09-check.sql`, `references/C10-check.sql` | Same values as the references |
| Model run | Help adapting the skeleton's `--run` options to my two questions on the five required models, with separate state and trace files | the `--run` command in `README.md` | Run by me: 10 real calls, 1 attempt each |
| Failure causes | Help reading the SQL returned by the failed cells | `explanation` column of `comparison-yehor-C09-C10.csv` | Each cause re-tested on the database (year-only query = 548920, partial C10 condition = 119410); qwen C10 checked against `extract_sql` in the skeleton |
| Repository | Help setting up the shared repository and a personal branch | initial `main` (kit, README), branch `yehor/work` | Fresh clone passes `check_access.py --no-network` |
