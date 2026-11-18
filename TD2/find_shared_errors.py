import csv
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parent.parent
trace_path = root / "TD1" / "kit-td1" / "traces-td1.csv"

with trace_path.open(encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))

# Keep the latest real attempt for each question and provider/model pair.
latest = {}

for row in rows:
    if row.get("nature", "").strip() != "real":
        continue

    key = (
        row["case_id"].strip(),
        row["provider"].strip(),
        row["model_requested"].strip(),
    )
    order = (
        row.get("date_utc", "").strip(),
        int(row.get("attempts") or 1),
    )

    if key not in latest or order >= latest[key][0]:
        latest[key] = (order, row)

# Group incorrect answers by question and returned value.
groups = defaultdict(list)

for _, row in latest.values():
    if row["verdict"].strip() == "incorrect" and row["value"].strip():
        key = (row["case_id"].strip(), int(row["value"]))
        groups[key].append(row)

found = False

for (case_id, value), answers in sorted(groups.items()):
    if len(answers) < 2:
        continue

    found = True
    print(f"\n{case_id}: shared incorrect value = {value}")

    for row in answers:
        print(
            f"  {row['provider']}:{row['model_requested']} "
            f"| reference = {row['reference']}"
        )

if not found:
    print("No shared incorrect value found among the latest real attempts.")