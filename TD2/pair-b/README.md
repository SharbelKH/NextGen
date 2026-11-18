# TD2 Pair B — shared wrong values

**C09 contribution:** Sherbal Al khouri.

The scan [`find_shared_errors.py`](find_shared_errors.py) reads the saved TD1
traces without new model calls. Its captured
[`shared-errors-output.txt`](shared-errors-output.txt) identifies C02, C09,
and C19. Run `python3 -B TD2/pair-b/find_shared_errors.py` from the repository
root to repeat it.

- **C02:** `c02-analysis.ipynb`, `c02-20b-delta.sql/.csv`, and
  `c02-dots-delta.sql/.csv` are the previously committed analysis, moved here
  together. The notebook locates the repository when opened from the root,
  `TD2/`, or `TD2/pair-b/`, and writes its result files here.
- **C09:** [`c09-analysis.md`](c09-analysis.md) explains the two saved model
  queries, the 2-of-3 and 3-of-5 vote, the independent reference, and the
  executed customer-level delta. The complete queries, diagnostic SELECT,
  CSV, and replay commands are linked there.
- **C19:** identified by the scan and the vote table; its SQL diagnosis and
  executed delta still need to be added by its owner.

The group's session report at `../reports/td2.md` should link to the three
cases and distinguish the saved outputs from the explanations of their causes.
