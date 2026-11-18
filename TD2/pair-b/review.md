# Pair B review of the other TD2 parts

This is Pair B's shared review document. It records the Pair A review below;
the team can add its Pair C review to this same file after checking the routing
policy and simulator. The review uses the stored TD1 experiment and offline
commands only.

## Pair A — vote and twenty-question comparison

### What we checked

- The [vote method](../pair-a/skeleton-multi-llm-en.py) against the TD2 contract:
  strict majority, one vote per provider/model pair, unavailable members kept
  in `n`, and abstention when no value reaches `k`.
- The [13 contract cases](../pair-a/test-vote.py), the fixed-panel workshop on
  C09, and the [comparison driver](../pair-a/vote-compare.py) on all 20 saved
  questions. The reference is compared after the vote.
- The [Pair A explanation](../pair-a/README.md) against the individual C09 and
  C19 SQL diagnoses in this folder.

### Findings, changes, and reasons

| Finding | Change | Why it improves the work |
|---|---|---|
| The comparison driver treated an absent TD1 model/question row as an unavailable voter. It could print a complete-looking 20-question table even if a trace file was incomplete. | Added `validate_batch` to `vote-compare.py`: require C01–C20 references and all five model cells for every question before writing the table. | A missing measurement is now reported as missing evidence. A recorded error or rejected SQL still remains in the declared panel without a vote. |
| The driver did not check whether the five final proposals for a question shared one prompt hash. | The same validation rejects missing or inconsistent hashes. | The table cannot quietly compare answers to different prompts as if they were one question. |
| The Pair A conclusion said two models shared the same wrong reading of completed age in C09 and C19. Their SQL errors differ within each case, although both pairs return zero. | Corrected the conclusion in `pair-a/README.md` to describe distinct faulty age predicates that converge on zero. | The explanation now separates observed agreement on a value from the causes found by reading the SQL. |

The core `vote_k_sur_n` method needed **no correction** in this review. It
returns the expected shapes and votes on the tested contract cases. We did
not change the stored TD1 traces, the declared panels, or the vote threshold.

### Verification

From the repository root:

```bash
python3 -B TD2/pair-a/test-vote.py
python3 -B TD2/pair-a/atelier-vote.py --traces TD1/kit-td1/traces-td1.csv --case C09
python3 -B TD2/pair-a/vote-compare.py
```

Observed: **13/13 tests pass**; C09's fixed 2-of-3 panel returns the wrong
zero with two votes against reference 487980. The completed comparison still
reports 16 correct, 2 wrong, 2 abstentions for 2-of-3; and 16 correct, 0
wrong, 4 abstentions for 3-of-5. The validation rejects a deliberately
missing model cell and a deliberately mismatched prompt hash before it writes
an output table. Thus the guard changes how incomplete inputs fail, without
changing the results for the complete saved batch.

### Limits and remaining work

- The fixed panel can return a wrong consensus (C09 and C19). The larger
  quorum abstains on those two cases but also abstains on C02, which the fixed
  panel answered correctly. Neither panel guarantees correctness.
- The driver uses the last real attempt in file order. The saved export is
  chronological per cell, but this code does not establish provenance for an
  arbitrary mixture of separate experiments that happen to share a prompt
  hash. Use one documented export per experiment.
- These are 20 questions from one batch, not an estimate of a general error
  rate. A fresh clone should rerun the commands above before final hand-in.

## Pair C — routing rule and simulator

Review to be added by Pair B after checking the rule, seven scenarios,
failure behavior, and before/after outputs. Record any fixes, their reasons,
and the commands used to verify them here.
