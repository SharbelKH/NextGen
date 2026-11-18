#!/usr/bin/env python3
"""TD 2, Pair A: the fixed 2-of-3 panel against the 3-of-5 quorum, on the twenty TD 1 questions.

Uses only the stored TD 1 traces (no network). For every question and every model, the last
attempt is kept; an attempt without an executed value (access error, rejected SQL) stays in n
without a vote. The decision is made first by `vote_k_sur_n`; the reference is compared after.

    python vote-compare.py      # writes vote-comparison.csv and vote-comparison.md next to this file
"""
import csv
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
TRACES = HERE.parents[1] / "TD1" / "kit-td1" / "traces-td1.csv"
REFERENCES = HERE.parents[1] / "TD1" / "kit-td1" / "reference-td1.csv"

PANEL_2_OF_3 = [
    ("groq", "openai/gpt-oss-120b"),
    ("openrouter", "cohere/north-mini-code:free"),
    ("groq", "qwen/qwen3.8-27b"),
]
QUORUM_3_OF_5 = PANEL_2_OF_3 + [
    ("groq", "openai/gpt-oss-20b"),
    ("openrouter", "dots-studio/dots-3-note-preview:free"),
]
SHORT = {"openai/gpt-oss-120b": "120b", "cohere/north-mini-code:free": "cohere", "qwen/qwen3.8-27b": "qwen",
         "openai/gpt-oss-20b": "20b", "dots-studio/dots-3-note-preview:free": "dots"}


def load_vote():
    spec = importlib.util.spec_from_file_location("skeleton", HERE / "skeleton-multi-llm-en.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return lambda proposals, k: module.Orchestrateur.vote_k_sur_n(None, proposals, k)


def last_attempts(rows):
    """Last row per (case, provider, model) in file order: the file is chronological per cell."""
    last = {}
    for row in rows:
        if row["nature"] == "real":
            last[(row["case_id"], row["provider"], row["model_requested"])] = row
    return last


def validate_batch(refs, last):
    """Fail before publishing a table if the saved TD1 experiment is incomplete."""
    expected = {f"C{i:02d}" for i in range(1, 21)}
    if set(refs) != expected:
        raise ValueError(f"Expected references for C01-C20; missing={sorted(expected - set(refs))}, "
                         f"extra={sorted(set(refs) - expected)}")

    missing = [(case, provider, model) for case in sorted(expected)
               for provider, model in QUORUM_3_OF_5 if (case, provider, model) not in last]
    if missing:
        raise ValueError(f"Missing {len(missing)} stored model/question cells, first: {missing[0]}")

    for case in sorted(expected):
        hashes = {last[(case, provider, model)]["prompt_sha256"]
                  for provider, model in QUORUM_3_OF_5}
        if "" in hashes or len(hashes) != 1:
            raise ValueError(f"Inconsistent or missing prompt hashes for {case}: {sorted(hashes)}")


def proposals(last, case, members):
    out = []
    for provider, model in members:
        row = last.get((case, provider, model), {})
        value = row.get("value", "")
        valid = row.get("verdict") in {"correct", "incorrect"} and value not in {None, ""}
        out.append(SimpleNamespace(provider=provider, model_requested=model,
                                   value=int(value) if valid else None,
                                   verdict="executed" if valid else "error",
                                   raw_verdict=row.get("verdict", "missing")))
    return out


def describe(decision, reference):
    if decision["consensus"]:
        ok = "correct" if decision["value"] == reference else "WRONG"
        return f"consensus {decision['value']} ({decision['votes']} votes, {ok})"
    return f"abstain (max {decision['votes']} votes)"


def main():
    vote = load_vote()
    rows = list(csv.DictReader(TRACES.open(encoding="utf-8-sig", newline="")))
    refs = {r["case_id"]: int(r["revenue_cents"]) for r in csv.DictReader(REFERENCES.open(encoding="utf-8-sig"))}
    last = last_attempts(rows)
    validate_batch(refs, last)
    table = []
    for case in sorted(refs):
        p3, p5 = proposals(last, case, PANEL_2_OF_3), proposals(last, case, QUORUM_3_OF_5)
        d3, d5 = vote(p3, 2), vote(p5, 3)
        per_model = "; ".join(f"{SHORT[p.model_requested]}={p.value if p.value is not None else p.raw_verdict}"
                              for p in p5)
        table.append({
            "case_id": case, "reference": refs[case], "proposals_5_models": per_model,
            "d23_consensus": d3["consensus"], "d23_value": d3["value"], "d23_votes": d3["votes"],
            "d23_vs_reference": "" if not d3["consensus"] else ("correct" if d3["value"] == refs[case] else "wrong"),
            "d35_consensus": d5["consensus"], "d35_value": d5["value"], "d35_votes": d5["votes"],
            "d35_vs_reference": "" if not d5["consensus"] else ("correct" if d5["value"] == refs[case] else "wrong"),
            "decision_changes": (d3["consensus"], d3["value"]) != (d5["consensus"], d5["value"]),
            "text23": describe(d3, refs[case]), "text35": describe(d5, refs[case]),
        })

    fields = [k for k in table[0] if not k.startswith("text")]
    with (HERE / "vote-comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: r[k] for k in fields} for r in table)

    lines = ["| Case | Reference | Last attempt of each model | 2-of-3 panel (k=2) | 3-of-5 quorum (k=3) | Changes |",
             "|---|---:|---|---|---|---|"]
    for r in table:
        lines.append(f"| {r['case_id']} | {r['reference']} | {r['proposals_5_models']} | {r['text23']} | "
                     f"{r['text35']} | {'**yes**' if r['decision_changes'] else 'no'} |")
    count = lambda key, val: sum(1 for r in table if r[key] == val)
    lines += ["",
              f"2-of-3: {count('d23_vs_reference', 'correct')} correct consensus, {count('d23_vs_reference', 'wrong')} wrong "
              f"consensus, {count('d23_consensus', False)} abstentions.",
              f"3-of-5: {count('d35_vs_reference', 'correct')} correct consensus, {count('d35_vs_reference', 'wrong')} wrong "
              f"consensus, {count('d35_consensus', False)} abstentions.",
              f"Decision changes between 2-of-3 and 3-of-5: {sum(r['decision_changes'] for r in table)} questions."]
    (HERE / "vote-comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
