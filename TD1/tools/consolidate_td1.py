"""Combine saved TD1 evidence offline. No database execution or API calls."""

import ast
import csv
import hashlib
import io
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "kit-td1"

# The shared traces-td1 files originally held only C01/C02. Keep their bytes
# before replacing those paths with the combined outputs.
ARCHIVE = KIT / "raw-c01-c02"
ARCHIVE.mkdir(exist_ok=True)
for filename in ("traces-td1.csv", "traces-td1.jsonl"):
    target = ARCHIVE / filename
    if not target.exists():
        shutil.copyfile(KIT / filename, target)

SOURCES = [
    "kit-td1/raw-c01-c02/traces-td1.csv",
    *[f"kit-td1/traces-mariem-{m}.csv" for m in ("120b", "20b", "cohere", "qwen", "dots")],
    "kit-td1/traces-valec-c05-c06-c17.csv",
    "kit-td1/adam-nasri-work/traces-c07-c08.csv",
    "yehor-nalyvaiko/traces/traces-yehor.csv",
    "oussama-meziane/traces-oussama.csv",
    "pablo-laxague/traces-td1.csv",
    "sharbel-khoury/traces-C15-C16-C20.csv",
    "sharbel-khoury/traces-dots-C07-C08.csv",
]


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


config = json.loads((KIT / "modeles-autorises.json").read_text())
models = [(m["gate"], m["identifiant_exact"]) for m in config["modeles"] if not m["optionnel"]]
questions = json.loads((KIT / "questions-td1.json").read_text())["questions"]
references = {r["case_id"]: r["revenue_cents"] for r in read_csv(KIT / "reference-td1.csv")}
expected = {(q["id"], provider, model) for q in questions for provider, model in models}

# Read the prompt constants as text; do not import or run the course skeleton.
constants = {}
for node in ast.parse((KIT / "skeleton-multi-llm-en.py").read_text()).body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in ("SYSTEM_PROMPT", "USER_PROMPT_TEMPLATE"):
                constants[target.id] = ast.literal_eval(node.value)
schema = (KIT / "schema.sql").read_text().strip()
expected_prompts = {}
for q in questions:
    user = constants["USER_PROMPT_TEMPLATE"].format(schema=schema, question=q["question"])
    expected_prompts[q["id"]] = hashlib.sha256((constants["SYSTEM_PROMPT"] + "\n" + user).encode()).hexdigest()

rows, provenance, grouped = [], [], defaultdict(list)
fields = None
for source in SOURCES:
    path = ROOT / source
    source_rows = read_csv(path)
    assert source_rows, f"Empty source: {source}"
    if fields is None:
        fields = list(source_rows[0])
    assert set(source_rows[0]) == set(fields), f"Headers differ: {source}"
    for index, row in enumerate(source_rows, 1):
        key = (row["case_id"], row["provider"], row["model_requested"])
        assert key in expected and row["nature"] == "real", (source, key)
        assert row["cell_id"] == f"{key[1]}:{key[2]}:{key[0]}", (source, "cell_id")
        assert row["reference"] == references[key[0]], (source, "reference")
        assert row["prompt_sha256"] == expected_prompts[key[0]], (source, "prompt")
        if row["verdict"] in ("correct", "incorrect"):
            assert (int(row["value"]) == int(row["reference"])) == (row["verdict"] == "correct")
        grouped[key].append((row, source))
        rows.append(row)
        provenance.append({"combined_record": len(rows), "source_file": source,
                           "source_record": index, "cell_id": row["cell_id"],
                           "attempts": row["attempts"], "date_utc": row["date_utc"],
                           "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})

assert set(grouped) == expected, f"Missing cells: {expected - set(grouped)}"
assert len(rows) == 108
latest = {}
for key, attempts in grouped.items():
    attempts.sort(key=lambda item: (int(item[0]["attempts"]), item[0]["date_utc"]))
    assert [int(r["attempts"]) for r, _ in attempts] == list(range(1, len(attempts) + 1))
    assert len(attempts) <= 2
    latest[key] = attempts[-1]

causes = {
    ("openai/gpt-oss-20b", "C02"): "Uses births in 2025-2026 instead of the one-year window for completed age 25.",
    ("cohere/north-mini-code:free", "C02"): "Requires the birthday to have passed in 2026. It misses customers born after 25 September 2000 who are still 25.",
    ("dots-studio/dots-3-note-preview:free", "C02"): "Keeps only births on 25 September 2001 and invents a one-day order period instead of using all orders.",
    ("qwen/qwen3.8-27b", "C03"): "Returned an unclosed markdown SQL fence. The extractor left it in the SQL and the sandbox rejected not_select; HTTP 200 was successful access.",
    ("cohere/north-mini-code:free", "C08"): "The birthday test mostly selects birthdays on or before 24 September without requiring the correct birth year, so it includes other ages.",
    ("cohere/north-mini-code:free", "C09"): "Compares the birth year minus a birthday adjustment with 25; it never subtracts the birth year from 2026.",
    ("qwen/qwen3.8-27b", "C09"): "Uses the order date instead of the reference date and requires month-day to be both >= and < the same birthday, so no row matches.",
    ("dots-studio/dots-3-note-preview:free", "C09"): "The birthday OR branches cover every birthday in birth year 2001. This reduces to a year-only age test.",
    ("cohere/north-mini-code:free", "C10"): "Casting a date string to INTEGER keeps its year, so age is computed without checking the birthday.",
    ("qwen/qwen3.8-27b", "C10"): "Returned an unclosed markdown SQL fence. The extractor left it in the SQL and the sandbox rejected not_select; HTTP 200 was successful access.",
    ("dots-studio/dots-3-note-preview:free", "C10"): "Keeps year difference 25 after the birthday but misses year difference 26 before the birthday, when the customer is still 25.",
    ("openai/gpt-oss-20b", "C11"): "Uses a five-year birth window from December 2001 to December 2006 instead of completed age 25.",
    ("cohere/north-mini-code:free", "C11"): "Uses births in 2025-2026 instead of subtracting 25/26 years and adds an unrequested December order period.",
    ("qwen/qwen3.8-27b", "C15"): "The birthday must be both <= 09-25 and > 09-25, so no customer matches. The birth year is not checked.",
    ("qwen/qwen3.8-27b", "C16"): "Wrong birthday boundaries: excludes customers turning 25 on the reference day and includes those turning 26 that day.",
    ("dots-studio/dots-3-note-preview:free", "C16"): "Birth dates after 25 September 2001 select customers younger than 25. The final birthday OR condition has no effect.",
    ("cohere/north-mini-code:free", "C17"): "Builds month-year instead of month-day with substr(birth_date,1,4), so the birthday adjustment is wrong.",
    ("qwen/qwen3.8-27b", "C17"): "Wrong birthday boundaries: excludes customers turning 25 on the reference day and includes those turning 26 that day.",
    ("dots-studio/dots-3-note-preview:free", "C18"): "Misses customers whose year difference is 26 but whose birthday has not happened yet; they are still 25 on the order date.",
    ("openai/gpt-oss-120b", "C19"): "Requires birth_date to equal the reference date minus 25 years, selecting only one birthday instead of a one-year range.",
    ("cohere/north-mini-code:free", "C19"): "Subtracts date strings and divides by 365. SQLite's numeric conversion does not give elapsed days, so the computed birth-date bounds are wrong.",
    ("qwen/qwen3.8-27b", "C19"): "Compares year strings to a full date with <= and does not enforce an upper age bound; customers older than 25 can match.",
}

comparison = []
for q in questions:
    for provider, model in models:
        row, source = latest[(q["id"], provider, model)]
        explanation = "Matches the teacher-provided reference."
        if row["verdict"] != "correct":
            explanation = causes[(model, q["id"])]
        if int(row["attempts"]) == 2:
            explanation += " Attempt 2 after HTTP 401; the OpenRouter key was corrected. Both attempts are retained."
        if row["date_utc"].startswith("2026-10-30"):
            explanation += " Late addition by Sherbal Al khouri on 30 October 2026; not part of the original session-day batch."
        comparison.append(dict(case_id=q["id"], model_id=f"{provider}:{model}",
                               trace_file="../" + source, cell_id=row["cell_id"], nature=row["nature"],
                               status=row["verdict"], value_cents=row["value"],
                               reference_cents=row["reference"], explanation=explanation))

write_csv(KIT / "traces-td1.csv", fields, rows)
with (KIT / "traces-td1.jsonl").open("w") as stream:
    for row in rows:
        record = dict(row)
        record["attempts"] = int(record["attempts"])
        record["latency_ms"] = float(record["latency_ms"]) if record["latency_ms"] else ""
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
write_csv(KIT / "trace-sources.csv", list(provenance[0]), provenance)
write_csv(KIT / "model-question-comparison-en.csv", list(comparison[0]), comparison)

# Copy the dated course portfolio rather than presenting live prices.
portfolio = read_csv(KIT / "portefeuille-modeles-2026-09-28.csv")
summary_fields = ["provider", "model_id", "public_index", "index_date", "index_source",
                  "paid_route_same_model", "input_usd_per_million", "output_usd_per_million",
                  "price_date", "price_source", "access_used", "period_results", "age_results",
                  "product_results", "combined_results", "trace_files", "limits"]
summary = []
stats = {}
for provider, model in models:
    results = [latest[(q["id"], provider, model)][0] for q in questions]
    stats[f"{provider}:{model}"] = Counter(r["verdict"] for r in results)
    matches = [p for p in portfolio if p["identifiant_gate"] == model]
    indexed = [p for p in matches if p["score_public"]]
    paid = [p for p in matches if p["acces"] == "payant"]
    row = dict.fromkeys(summary_fields, "")
    row.update(provider=provider, model_id=model,
               public_index=indexed[0]["score_public"] if indexed else "N/A",
               index_date="2026-09-28" if indexed else "",
               index_source="portefeuille-modeles-2026-09-28.csv" if indexed else "N/A: no index in the supplied dated portfolio",
               paid_route_same_model=paid[0]["gate"] if paid else "N/A: no paid route for this exact model documented in the supplied portfolio",
               input_usd_per_million=paid[0]["prix_entree_usd_m"] if paid else "N/A",
               output_usd_per_million=paid[0]["prix_sortie_usd_m"] if paid else "N/A",
               price_date="2026-09-28" if paid else "",
               price_source="portefeuille-modeles-2026-09-28.csv (dated course snapshot; not a live quote)" if paid else "N/A: no matching paid-route price in supplied evidence",
               access_used="Groq Free" if provider == "groq" else "OpenRouter :free; zero-price cap",
               trace_files="traces-td1.csv; trace-sources.csv",
               limits="20 final cells; one sample per cell. Categories are disjoint by question type. Zero final access failures. No general ranking.")
    for family, predicate in (
        ("period_results", lambda t: t == "period"),
        ("age_results", lambda t: t.startswith("age") and "+" not in t),
        ("product_results", lambda t: t == "product list"),
        ("combined_results", lambda t: "+" in t),
    ):
        subset = [latest[(q["id"], provider, model)][0] for q in questions if predicate(q["type"])]
        counts = Counter(r["verdict"] for r in subset)
        row[family] = (f"{counts['correct']}/{len(subset)} correct; {counts['incorrect']} incorrect; "
                       f"{counts['sql_rejected']} rejected; {counts['access_error']} access_error; 0 unfinished")
    if model == "dots-studio/dots-3-note-preview:free":
        row["limits"] += " C07/C08 completed on 30 October; earlier Dots cells were run on 21 October."
    summary.append(row)
write_csv(KIT / "five-model-summary-en.csv", summary_fields, summary)

matrix = ["# TD 1 comparison matrix", "", "Final verdict per cell. See [comparison CSV](../kit-td1/model-question-comparison-en.csv) for values and causes.", "", "C = correct; I = incorrect; R = SQL rejected. Dots C07/C08 are additions from 30 October.", "",
          "| Model | " + " | ".join(q["id"] for q in questions) + " |",
          "|---|" + "---|" * len(questions)]
for provider, model in models:
    marks = [{"correct": "C", "incorrect": "I", "sql_rejected": "R"}[latest[(q["id"], provider, model)][0]["verdict"]] for q in questions]
    matrix.append(f"| {provider}:{model} | " + " | ".join(marks) + " |")
(ROOT / "reports" / "td1-matrix.md").write_text("\n".join(matrix) + "\n")
print(json.dumps({"attempts": len(rows), "cells": len(comparison), "final_results": stats}, indent=2))
