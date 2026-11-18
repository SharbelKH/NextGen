
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
