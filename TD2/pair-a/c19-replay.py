"""C19 replay: stored model SQL, independent check and delta, read only.

Run from the repository root: python3 -B TD2/pair-a/c19-replay.py
Writes TD2/pair-a/c19-results.txt and TD2/pair-a/c19-delta.csv.
"""
import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE.parents[1] / "TD1" / "kit-td1" / "data" / "boutique.sqlite"
REFERENCE = 1990


def scalar(db, sql):
    return db.execute(sql).fetchone()[0]


def main():
    db = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
    gpt120b = scalar(db, (HERE / "c19-120b-as-returned.sql").read_text(encoding="utf-8"))
    north = scalar(db, (HERE / "c19-north-as-returned.sql").read_text(encoding="utf-8"))
    cohort = db.execute(
        "SELECT customer_id, birth_date FROM customers "
        "WHERE birth_date > '2000-09-25' AND birth_date <= '2001-09-25' ORDER BY birth_date").fetchall()
    exact_day = db.execute(
        "SELECT customer_id FROM customers WHERE birth_date = date('2026-09-25', '-25 years')").fetchall()
    north_pieces = db.execute(
        "SELECT '2026-09-25' - '2001-09-24', ('2026-09-25' - '2001-09-24') / 365, "
        "date('2026-09-25', '-0 years'), date('2026-09-25', '-1 years')").fetchone()
    cursor = db.execute((HERE / "c19-delta.sql").read_text(encoding="utf-8"))
    header = [d[0] for d in cursor.description]
    rows = cursor.fetchall()
    with open(HERE / "c19-delta.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)
    total = sum(r[2] for r in rows)
    lines = [
        "C19 replay on TD1/kit-td1/data/boutique.sqlite (SQLite, read only)",
        f"GPT-OSS 120B stored SQL: {gpt120b} cents",
        f"North Mini Code stored SQL: {north} cents",
        f"Reference (reference-td1.csv): {REFERENCE} cents",
        f"Customers exactly 25 on 2026-09-25: {len(cohort)} "
        + ", ".join(f"{c} {b}" for c, b in cohort),
        f"Customers born on 2001-09-25 exactly (GPT-OSS 120B cohort): {len(exact_day)} "
        + ", ".join(c for (c,) in exact_day),
        "North age expression for a birth date 2001-09-24: "
        f"'2026-09-25' - '2001-09-24' = {north_pieces[0]}, / 365 = {north_pieces[1]}, "
        f"window ({north_pieces[3]}, {north_pieces[2]}]",
        f"Delta SELECT: {len(rows)} eligible customer(s) with product d orders in September",
        f"Sum(reference_revenue_cents): {total} cents",
        f"Sum(gpt120b_missed_cents): {sum(r[3] for r in rows)} cents",
        f"Sum(north_missed_cents): {sum(r[4] for r in rows)} cents",
        f"Reference minus GPT-OSS 120B: {REFERENCE - gpt120b} cents; "
        f"reference minus North: {REFERENCE - north} cents",
    ]
    (HERE / "c19-results.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    assert total == REFERENCE, "independent cohort sum differs from the reference"


if __name__ == "__main__":
    main()
