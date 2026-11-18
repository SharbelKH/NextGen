# TD 2 — Pair A: the k-of-n vote

**Pair A:** Yehor Nalyvaiko (`yehor-na`), Oussama Meziane, Adam Nasri.

Subject TD 2 ("vote and route", 18 November 2026), stored in the group's `TD3/` folder.
Input: the merged TD 1 traces `../../TD1/kit-td1/traces-td1.csv` (100 cells, 108 rows, all `real`) and
`../../TD1/kit-td1/reference-td1.csv`. No new network call.

## Files

| File | Content |
|---|---|
| `skeleton-multi-llm-en.py` | copy of the group skeleton (TD 1 version) with `Orchestrateur.vote_k_sur_n` completed |
| `atelier-vote.py`, `sandbox_sqlite.py` | kit files, unchanged, copied next to the skeleton so the workshop loads our vote |
| `test-vote.py` → `out-tests.txt` | 13 contract tests (agreement, disagreement, unavailable members, duplicate routes, invalid k) |
| `out-synthetic.txt` | `atelier-vote.py` on its four synthetic examples |
| `out-real-2of3.txt` | `atelier-vote.py --traces … --case` on C10, C09, C17, C02, C19 |
| `vote-compare.py` → `vote-comparison.md`, `vote-comparison.csv` | the driver: 2-of-3 panel against 3-of-5 quorum on C01–C20 |

Replay (from this folder):

    python atelier-vote.py
    python test-vote.py
    python atelier-vote.py --traces ../../TD1/kit-td1/traces-td1.csv --case C10
    python vote-compare.py

## The vote

`vote_k_sur_n(traces_question, k)`, following the docstring contract:

1. `n` is the number of panel members, whatever their state. `n // 2 < k <= n` is checked first, otherwise `ValueError`.
2. A second proposal from the same `provider:model_requested` raises `ValueError`: one model, one vote.
3. Only proposals with `verdict == "executed"` and a value vote. An error, a rejected SQL or an access failure stays in `n`
   without a vote, so it makes a majority harder to reach.
4. Votes are counted per value. If a value has at least `k` votes it is returned with its votes and the agreeing models.
   As `k` is a strict majority, at most one value can reach it.
5. Otherwise the vote abstains: `value = None`, `votes` = the largest count (0 if nobody voted). It never picks the most
   frequent value below `k` and never draws lots.

The vote never receives the reference: the comparison with `reference-td1.csv` happens after the decision.

Declared panels:
- **2-of-3**: fixed panel of `atelier-vote.py` — `groq:openai/gpt-oss-120b`, `openrouter:cohere/north-mini-code:free`,
  `groq:qwen/qwen3.8-27b`, `k = 2`.
- **3-of-5**: the five TD 1 models (panel above + `groq:openai/gpt-oss-20b`, `openrouter:dots-studio/dots-3-note-preview:free`), `k = 3`.

For each model the last attempt of the cell is used (the merged file is chronological per cell; the eight access errors
of the first attempts were all followed by a successful second attempt). An attempt counts as a vote only when its verdict
is `correct` or `incorrect` with a value; `sql_rejected` (Qwen C03, Qwen C10) is an unavailable member.

## Test outputs

All 13 tests pass (`out-tests.txt`). The four synthetic examples of `atelier-vote.py` (`out-synthetic.txt`):
agreement → consensus 100; disagreement → abstain (1 vote); unavailable `[100, None, None]` → abstain (1 vote, the two
errors stay in n = 3); wrong consensus `[0, 0, 100]` → consensus 0, wrong against the reference 100.

## Twenty decisions: 2-of-3 against 3-of-5

Full table with the last value of each model: `vote-comparison.md`.

| Case | Ref. | 2-of-3 (k=2) | 3-of-5 (k=3) | Change |
|---|---:|---|---|---|
| C01 | 792800 | 792800 (3) ✓ | 792800 (5) ✓ | no |
| C02 | 590320 | 590320 (2) ✓ | abstain (2) | **yes** |
| C03 | 936350 | 936350 (2) ✓ | 936350 (4) ✓ | no |
| C04 | 2826250 | 2826250 (3) ✓ | 2826250 (5) ✓ | no |
| C05 | 38480 | 38480 (3) ✓ | 38480 (5) ✓ | no |
| C06 | 0 | 0 (3) ✓ | 0 (5) ✓ | no |
| C07 | 13970 | 13970 (3) ✓ | 13970 (5) ✓ | no |
| C08 | 605580 | 605580 (2) ✓ | 605580 (4) ✓ | no |
| C09 | 487980 | **0 (2) ✗** | abstain (2) | **yes** |
| C10 | 558980 | abstain (1) | abstain (2) | no |
| C11 | 446690 | 446690 (2) ✓ | 446690 (3) ✓ | no |
| C12 | 1666490 | 1666490 (3) ✓ | 1666490 (5) ✓ | no |
| C13 | 107740 | 107740 (3) ✓ | 107740 (5) ✓ | no |
| C14 | 0 | 0 (3) ✓ | 0 (5) ✓ | no |
| C15 | 168680 | 168680 (2) ✓ | 168680 (4) ✓ | no |
| C16 | 376740 | 376740 (2) ✓ | 376740 (3) ✓ | no |
| C17 | 258180 | abstain (1) | 258180 (3) ✓ | **yes** |
| C18 | 62480 | 62480 (3) ✓ | 62480 (4) ✓ | no |
| C19 | 1990 | **0 (2) ✗** | abstain (2) | **yes** |
| C20 | 1106090 | 1106090 (3) ✓ | 1106090 (5) ✓ | no |

(n) = number of votes for the value kept, or the largest count when the vote abstains.

| | correct consensus | wrong consensus | abstentions |
|---|---:|---:|---:|
| 2-of-3 panel | 16 | **2** (C09, C19) | 2 (C10, C17) |
| 3-of-5 quorum | 16 | **0** | 4 (C02, C09, C10, C19) |

### The four questions where the decision changes

- **C09** (age on 2026-09-26). Panel: Cohere 0 and Qwen 0 agree, 120B 487980 is outvoted → wrong consensus 0.
  Quorum: 487980 (120B, 20B) 2 votes, 0 (Cohere, Qwen) 2 votes, Dots 548920 → no value reaches 3 → abstain.
  The two extra models do not give the right answer a majority, but they stop the wrong one.
- **C19** (product d, age on 2026-09-25). Panel: 120B 0 and Cohere 0 → wrong consensus 0; Qwen 83580.
  Quorum: 0 (120B, Cohere) 2, 1990 (20B, Dots) 2, 83580 → abstain. Same mechanism as C09.
- **C02** (age on 2026-09-25). Panel: 120B and Qwen 590320 → correct consensus; Cohere 321340.
  Quorum: 590320 (2), but 20B and Dots agree on the wrong value 0 (2), Cohere 321340 → abstain.
  Here the larger quorum loses a correct answer: a wrong agreement outside the panel blocks the majority.
- **C17** (products a, b, c, period, age). Panel: 120B 258180, Cohere 197080, Qwen 248490 → three different values → abstain.
  Quorum: 20B and Dots also return 258180 → 3 votes → correct consensus.

### Unchanged but worth noting

- **C10**: Qwen's SQL was rejected by the sandbox (`sql_rejected`, HTTP 200). Qwen stays in n without a vote. Panel: 120B 558980,
  Cohere 548920 → 1 vote each → abstain. Quorum: 558980 (120B, 20B) 2 votes < 3 → abstain. This is the question we use to show
  an abstention on real traces (`out-real-2of3.txt`).
- **C03**: Qwen also rejected; 120B and Cohere still reach 2 of 3, the failed member costs nothing here.
- No access error remains in the last attempts: the eight first-attempt failures were all OpenRouter HTTP 401 (bad key:
  Cohere C15, C16, C20; Dots C07, C08, C15, C16, C20), retried once with success, so the vote uses the second attempt for
  those cells. There was no HTTP 429 in the batch, so no vote margin is shifted by a rate limit.

## What we conclude

- With these traces the 3-of-5 quorum makes **no wrong decision** (0 against 2 for the panel), at the price of **two more
  abstentions** (4 against 2). It also recovers one question the panel could not decide (C17) and loses one it decided
  correctly (C02).
- Every wrong consensus comes from **age questions** (C09, C19) where two models share the same wrong reading of
  "completed age". Agreement is not proof: the panel's 2 votes on 0 are as strong as 2 votes on the right value.
- An abstention is a correct output of the vote, not a failure: the system says it cannot decide instead of inventing a value.
- Limits: 20 questions and one run per model. These counts describe this batch only; they give neither a general error rate
  nor a guarantee that a quorum avoids wrong answers.

AI assistance was used for the code and the analysis; every result was rerun and checked (tests, workshop output, fresh clone).
