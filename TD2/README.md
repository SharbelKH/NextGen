# TD2 — vote and route (18 November 2026)

Course TD 2: the k-of-n vote, the wrong consensus and the routing rule. It works on the stored TD 1 traces
(`../TD1/kit-td1/traces-td1.csv`) and `../TD1/kit-td1/reference-td1.csv`; no new model calls.
Assignment: https://storage.googleapis.com/docs.g.quanticfactory.io/ESILV/next-generation-ai/latest/students/kit-td1/enonce-td2-en.html

| Folder                              | Step                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| [`pair-a/`](pair-a/README.md)       | Step 1 — `vote_k_sur_n`, tests, 2-of-3 panel against 3-of-5 quorum on the twenty questions |
| [`pair-b/`](pair-b/c09-analysis.md) | Step 2 — shared wrong values, faulty SQL clauses, executed delta queries                   |
| `pair-c/`                           | Step 3 — routing rule and `atelier-routage.py`                                             |

## Pair B — shared wrong values

[`pair-b/find_shared_errors.py`](pair-b/find_shared_errors.py) scans the saved
TD1 traces; its [output](pair-b/shared-errors-output.txt) identifies C02, C09,
and C19. Replay from the repository root with
`python3 -B TD2/pair-b/find_shared_errors.py`.

- **C02:** [analysis notebook](pair-b/c02-analysis.ipynb), with the GPT-OSS 20B
  and Dots delta SQL and CSV files in `pair-b/`.
- **C09 — Sherbal Al khouri:** [analysis and replay commands](pair-b/c09-analysis.md),
  both complete saved model queries, an independent reference check, and the
  [executed customer-level delta](pair-b/c09-delta.csv).
- **C19 — Pablo Laxague:** [analysis and replay command](pair-b/Pablo.ipynb), both
  complete saved model queries and the [executed customer-level delta](pair-b/Pablo.ipynb).

Pair B's [review of Pair A](pair-b/review.md) records checks, fixes, verified
results, and remaining limitations. Pair B will add its Pair C review to the
same document after reviewing the routing work.

The session report is `reports/td2.md`. Hand-in: Sunday 22 November 2026, 23:59.



