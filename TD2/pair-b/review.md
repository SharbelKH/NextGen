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

| Finding                                                                                                                                                                          | Change                                                                                                                                        | Why it improves the work                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| The comparison driver treated an absent TD1 model/question row as an unavailable voter. It could print a complete-looking 20-question table even if a trace file was incomplete. | Added `validate_batch` to `vote-compare.py`: require C01–C20 references and all five model cells for every question before writing the table. | A missing measurement is now reported as missing evidence. A recorded error or rejected SQL still remains in the declared panel without a vote. |
| The driver did not check whether the five final proposals for a question shared one prompt hash.                                                                                 | The same validation rejects missing or inconsistent hashes.                                                                                   | The table cannot quietly compare answers to different prompts as if they were one question.                                                     |
| The Pair A conclusion said two models shared the same wrong reading of completed age in C09 and C19. Their SQL errors differ within each case, although both pairs return zero.  | Corrected the conclusion in `pair-a/README.md` to describe distinct faulty age predicates that converge on zero.                              | The explanation now separates observed agreement on a value from the causes found by reading the SQL.                                           |

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

### What we checked

- The adapted [`atelier-routage.py`](../pair-c/atelier-routage.py) against the TD2 routing requirements: TD1-based eligibility, cheapest eligible first model, verification according to the use case, deferral and abstention.
- The eight question families in `TD1_RESULTS`, including their supporting cells and observed correct/total ratios.
- The seven simulator scenarios: simple, complex, deferrable, urgent, budget exhausted, high impact and unknown capability.
- The original and adapted simulator outputs (`results-before.txt` and `results-after.txt`), together with the individual deferrable output.
- The `choose` function's priority order and the traceability of its routing decisions.

### Findings, changes, and reasons

| Finding                                                                                                                                                                                                                                                                  | Change / recommendation                                                                                                                                                           | Why it improves the work                                                                                                                                                                                   |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The adapted simulator correctly replaces the original abstract difficulty levels with question-family eligibility based on observed TD1 accuracy.                                                                                                                        | No correction required for this main adaptation.                                                                                                                                  | Model selection is now justified by the group's actual TD1 results rather than generic capability assumptions.                                                                                             |
| The eligibility filter only accepts models with 100% observed accuracy on a family.                                                                                                                                                                                      | Keep this conservative policy, but explicitly explain that models with lower accuracy are excluded even when additional verification could potentially make their use acceptable. | This makes the safety-versus-cost trade-off explicit and avoids presenting the eligibility threshold as a requirement imposed directly by the assignment.                                                  |
| The `FIRST_MODEL` dictionary hardcodes a preferred model for each family. The sorting function prioritises this model before comparing cash costs.                                                                                                                       | Verify each preferred model against the portfolio prices and document why it is the cheapest eligible option.                                                                     | The assignment requires the first model to be the cheapest model supported by the TD1 results. The supplied files do not include enough portfolio price information to independently confirm every choice. |
| Customer-facing requests specify a 2-of-3 quorum, but `choose` only selects one model and returns the verification requirement as a string.                                                                                                                              | Clarify that `checks` describes a required downstream verification step, not a quorum already executed by the simulator.                                                          | This prevents a routing decision from being mistaken for a completed verification.                                                                                                                         |
| The adapted resource definitions set all three models as free, with zero allocation and no quota reset.                                                                                                                                                                  | Check the resource definitions against the actual portfolio and include the relevant subscription allocation and API costs where applicable.                                      | This would make the adapted simulator more representative of the resource choices and cost constraints required by the assignment.                                                                         |
| The simulator checks immediately available eligible resources before considering deferral. However, the distinction between included subscription capacity, exhausted free capacity and paid capacity is not explicitly represented in the adapted resource definitions. | Explain the priority order and add a scenario comparing immediately available subscription capacity with an exhausted free resource whose quota resets before the deadline.       | This directly addresses the assignment's requirement to explain why available subscription capacity can be preferred to waiting, and when this priority should be reversed.                                |
| The seven scenarios cover the main routing outcomes, but do not test every relevant priority and verification case.                                                                                                                                                      | Add tests for available subscription capacity versus free quota deferral, and for customer-facing requests requiring a quorum.                                                    | These tests would provide stronger evidence that the routing policy behaves as intended in less straightforward situations.                                                                                |
| The routing reasons include the selected model, its TD1 score and the supporting question cells.                                                                                                                                                                         | No correction required for this traceability mechanism.                                                                                                                           | Each decision can be related to observed experimental evidence, as required by the assignment.                                                                                                             |

### Verification

Using the supplied offline execution results:

- **Simple:** GPT-20B is selected for F1, with 6/6 correct answers on C01, C04-C07 and C20.
- **Complex:** GPT-120B is selected for F2, with 4/4 correct answers on C02, C08, C09 and C11.
- **Deferrable:** GPT-120B is deferred for 60 minutes because it is unavailable and its quota is expected to reset within the 120-minute deadline.
- **Urgent:** The simulator abstains because no eligible model is available within the deadline.
