
# Pair C — Routing Policy

## 1. TD1 Accuracy

We compare five models on the 20 TD1 questions.
Each score is correct answers / total cases.

| Family | TD1 cells | GPT-120B | GPT-20B | Cohere | Qwen | Dots |
|---|---|---|---|---|---|---|
| F1 | C01,C04-C07,C20 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| F2 | C02,C08,C09,C11 | 4/4 | 2/4 | 0/4 | 3/4 | 2/4 |
| F2b | C10 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| F3 | C12 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 |
| F1+F3 | C03,C13,C14,C19 | 3/4 | 4/4 | 3/4 | 2/4 | 4/4 |
| F1+F2 | C15,C18 | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 |
| F2+F3 | C16 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 |
| F1+F2+F3 | C17 | 1/1 | 1/1 | 0/1 | 0/1 | 1/1 |

## 2. First Model Selection

The portfolio lists GPT-120B, GPT-20B and Qwen
on Groq as free (€0). Cohere and Dots were tested
in TD1 but are absent from the portfolio.

We select a free model with 100% TD1 accuracy
on the family. For equal prices, we prefer GPT-20B.

| Family | First model | TD1 result |
|---|---|---|
| F1 | GPT-20B | 6/6 |
| F2 | GPT-120B | 4/4 |
| F2b | GPT-20B | 1/1 |
| F3 | GPT-20B | 1/1 |
| F1+F3 | GPT-20B | 4/4 |
| F1+F2 | GPT-20B | 2/2 |
| F2+F3 | GPT-20B | 1/1 |
| F1+F2+F3 | GPT-20B | 1/1 |

## 3. Checking Rules

| Use case | Verification |
|---|---|
| Internal dashboard | None only if selected model scored 100% in TD1; otherwise 2-of-3 quorum or reference |
| Customer-facing figure | 2-of-3 quorum; reference if disagreement remains |
| Payout amount | Deterministic reference; otherwise review |

A 2-of-3 quorum requires at least two matching answers.
If checking fails, use a reference, request review,
or abstain. Never return an unchecked high-risk amount.

## 4. Fallback Rules

1. Try the next available model with 100% TD1 accuracy
   on the same family.
2. If free quotas are exhausted, defer until refill
   when the deadline allows.
3. If no safe option is available, abstain.

Verification requirements remain unchanged after
switching models.

An immediately available eligible resource is preferred
over waiting, unless a non-urgent request can safely
wait for a free quota refill before its deadline.

**Limitation:** These 20 questions support only a
batch-specific hypothesis, not a permanent model ranking
or a guarantee that quorum decisions are correct.
