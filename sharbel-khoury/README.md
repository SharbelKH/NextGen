# Sharbel Khoury — TD 1: C15, C16 and C20

`queries.py` contains the proposed reference queries for C15 and C16. It opens
the shared kit database in read-only mode and currently executes C16.

From the repository root:

```bash
python3 sharbel-khoury/queries.py
```

C15 returned 168680 cents and C16 returned 376740 cents in my local runs.
Both match the values given by the teacher. The teacher then asked us to use
the provided references and focus on testing the models. This is an answer-key
check, not an independent calculation.

## Model runs

I tested the five required models on C15, C16 and C20 on 21 October 2026.
I used the teacher's reference values in `../kit-td1/reference-td1.csv`.
All calls in these traces are real.

From `kit-td1`, the initial command was:

```bash
python3 skeleton-multi-llm-en.py --run --cases C15,C16,C20 --state ../sharbel-khoury/state-C15-C16-C20.jsonl --out ../sharbel-khoury/traces-C15-C16-C20.csv
```

The first run made 15 calls. All six OpenRouter calls failed with HTTP 401.
After replacing my OpenRouter key and checking account authentication, I
retried only those six cells using the same state and output files:

```bash
python3 skeleton-multi-llm-en.py --run --cases C15,C16,C20 --models openrouter:cohere/north-mini-code:free openrouter:dots-studio/dots-3-note-preview:free --state ../sharbel-khoury/state-C15-C16-C20.jsonl --out ../sharbel-khoury/traces-C15-C16-C20.csv
```

The supplied runner skipped saved HTTP 401 failures. Codex adjusted it so an
explicit resume can retry these after fixing the key. The existing maximum
of two attempts per cell is still enforced. The change is in the repository
diff for `../kit-td1/skeleton-multi-llm-en.py`.

## Results

| Model | C15 | C16 | C20 | Correct |
|---|---|---|---|---|
| Groq GPT-OSS 120B | correct | correct | correct | 3/3 |
| Groq GPT-OSS 20B | correct | correct | correct | 3/3 |
| OpenRouter North Mini Code | correct | correct | correct | 3/3 |
| Groq Qwen | incorrect | incorrect | correct | 1/3 |
| OpenRouter Dots | correct | incorrect | correct | 2/3 |

There were 12 correct final answers out of 15. These results only cover my
three questions, so they do not establish a general model ranking.

The three wrong answers came from age filters:

- Qwen C15 returned 0 instead of 168680. Its birthday conditions contradict
  each other, so no customer can match. It also does not check the birth year.
- Qwen C16 returned 367050 instead of 376740. It gets the birthday boundaries
  wrong for customers born exactly on 25 September.
- Dots C16 returned 218760 instead of 376740. It selects customers younger
  than 25, and its final month-day condition does not filter anything.

The original authentication failures are access errors, not wrong answers.
They are kept in the raw traces. The comparison uses the last attempt per cell.
The causes above come from reading the recorded SQL; I did not run extra
model calls to investigate them.

## Saved evidence

- `traces-C15-C16-C20.csv`: all 21 attempts (15 initial calls and six retries).
- `state-C15-C16-C20.jsonl`: the matching saved state, retaining attempt history.
- `comparison-sharbel-C15-C16-C20.csv`: 15 final results, with raw trace links
  and explanations. This follows the course comparison template.

Groq native costs are missing and should stay blank. OpenRouter free calls
that succeeded report zero cost. Missing cost is not the same as zero cost.
The group still needs to combine contributions and complete the five-model
portfolio summary and session report.

## AI assistance

I used Codex to help build and understand the reference queries, adapt the
database path, diagnose the authentication problem, change the resume rule,
and prepare the comparison and this write-up. I ran the course scripts myself.
Codex read the saved traces to explain the SQL errors; it did not run model calls.
