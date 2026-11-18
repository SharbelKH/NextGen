#!/usr/bin/env python3
"""TD 2 and TD 3: read the decisions of a routing rule, then adapt it to your own.

Synthetic resources, no API call, no key.

Costs are fictional USD excluding tax per request, with a fixed token envelope.
Capability levels 1/2/3 describe eligibility for this exercise, not model IQ.
Quota availability is supplied as a scenario, not measured from a provider.
"""
import argparse
import json


# TD2 Pair C - models from our TD1 evaluation
# Availability is simulated, not retrieved from the providers.

RESOURCES = [
    {
        "id": "GPT-20B",
        "access": "free",
        "available": True,
        "cash": 0.0,
        "allocation": 0.0,
        "reset_minutes": None,
    },
    {
        "id": "GPT-120B",
        "access": "free",
        "available": True,
        "cash": 0.0,
        "allocation": 0.0,
        "reset_minutes": None,
    },
    {
        "id": "Qwen",
        "access": "free",
        "available": True,
        "cash": 0.0,
        "allocation": 0.0,
        "reset_minutes": None,
    },
]

# TD1 results: number of correct answers / total questions
# These results come from our Pair C routing policy.

TD1_RESULTS = {
    "F1": {
        "cells": "C01,C04-C07,C20",
        "GPT-20B": (6, 6),
        "GPT-120B": (6, 6),
        "Qwen": (6, 6),
    },
    "F2": {
        "cells": "C02,C08,C09,C11",
        "GPT-20B": (2, 4),
        "GPT-120B": (4, 4),
        "Qwen": (3, 4),
    },
    "F2b": {
        "cells": "C10",
        "GPT-20B": (1, 1),
        "GPT-120B": (1, 1),
        "Qwen": (0, 1),
    },
    "F3": {
        "cells": "C12",
        "GPT-20B": (1, 1),
        "GPT-120B": (1, 1),
        "Qwen": (1, 1),
    },
    "F1+F3": {
        "cells": "C03,C13,C14,C19",
        "GPT-20B": (4, 4),
        "GPT-120B": (3, 4),
        "Qwen": (2, 4),
    },
    "F1+F2": {
        "cells": "C15,C18",
        "GPT-20B": (2, 2),
        "GPT-120B": (2, 2),
        "Qwen": (1, 2),
    },
    "F2+F3": {
        "cells": "C16",
        "GPT-20B": (1, 1),
        "GPT-120B": (1, 1),
        "Qwen": (0, 1),
    },
    "F1+F2+F3": {
        "cells": "C17",
        "GPT-20B": (1, 1),
        "GPT-120B": (1, 1),
        "Qwen": (0, 1),
    },
}

FIRST_MODEL = {
    "F1": "GPT-20B",
    "F2": "GPT-120B",
    "F2b": "GPT-20B",
    "F3": "GPT-20B",
    "F1+F3": "GPT-20B",
    "F1+F2": "GPT-20B",
    "F2+F3": "GPT-20B",
    "F1+F2+F3": "GPT-20B",
}



def choose(request, resources):
    """Route a request using the Pair C TD1 policy."""

    family = request.get("family")
    use_case = request.get("use_case", "internal")

    # 1. Identify the question family.
    if family not in TD1_RESULTS:
        return {
            "action": "abstain",
            "resource": None,
            "cash": 0,
            "checks": "manual review",
            "reason": f"Unknown TD1 family: {family}; no supporting TD1 cells",
        }

    results = TD1_RESULTS[family]
    cells = results["cells"]

    # 2. Determine required verification.
    if use_case == "payout":
        checks = "deterministic reference; otherwise human review"
    elif use_case == "customer":
        checks = "2-of-3 quorum; reference if disagreement"
    elif use_case == "internal":
        checks = "none for 100% TD1 accuracy; otherwise quorum or reference"
    else:
        return {
            "action": "abstain",
            "resource": None,
            "cash": 0,
            "checks": "manual review",
            "reason": f"Unknown use case for {family} ({cells})",
        }

    # 3. Only use models with 100% observed TD1 accuracy.
    eligible = []
    for resource in resources:
        model = resource["id"]
        score = results.get(model)

        if score is not None and score[0] == score[1]:
            eligible.append(resource)

    # 4. Prefer the model chosen by the routing policy.
    preferred = FIRST_MODEL[family]
    eligible.sort(
        key=lambda r: (
            r["id"] != preferred,
            r["cash"],
            r["id"] != "GPT-20B",
            r["id"],
        )
    )

    # 5. Try an available eligible model first.
    available = [
        r for r in eligible
        if r["available"] and r["cash"] <= request["budget"]
    ]

    if available:
        chosen = available[0]
        score = results[chosen["id"]]
        return {
            "action": "run",
            "resource": chosen["id"],
            "cash": chosen["cash"],
            "checks": checks,
            "reason": (
                f"{chosen['id']} scored {score[0]}/{score[1]} "
                f"on {family} (TD1 cells: {cells}); "
                f"available within budget"
            ),
        }

    # 6. Wait for a free quota reset if permitted.
    waiting = [
        r for r in eligible
        if not r["available"]
        and r["cash"] == 0
        and r["reset_minutes"] is not None
        and request["can_wait"]
        and 0 < r["reset_minutes"] <= request["deadline_minutes"]
    ]

    if waiting:
        chosen = min(waiting, key=lambda r: r["reset_minutes"])
        return {
            "action": "defer",
            "resource": chosen["id"],
            "cash": 0,
            "checks": checks,
            "reason": (
                f"{chosen['id']} eligible for {family} "
                f"(TD1 cells: {cells}); "
                "recheck availability after quota reset"
            ),
            "wake_in_minutes": chosen["reset_minutes"],
        }

    # 7. No safe model is available.
    return {
        "action": "abstain",
        "resource": None,
        "cash": 0,
        "checks": checks,
        "reason": (
            f"No eligible model for {family} within deadline "
            f"and budget (TD1 cells: {cells})"
        ),
    }


def scenarios():
    # Simulated requests and quotas, not real provider data.
    base = {
        "family": "F1",
        "use_case": "internal",
        "can_wait": True,
        "deadline_minutes": 120,
        "budget": 0.30,
    }

    # All free models are temporarily unavailable.
    exhausted = [
        dict(r, available=False, reset_minutes=60)
        for r in RESOURCES
    ]

    return [
        ("simple", base, RESOURCES),

        ("complex",
         {**base, "family": "F2"},
         RESOURCES),

        ("deferrable",
         {**base, "family": "F2"},
         exhausted),

        ("urgent",
         {**base, "family": "F2",
          "can_wait": False, "deadline_minutes": 5},
         exhausted),

        ("budget exhausted",
         {**base, "family": "F2",
          "can_wait": False, "budget": 0},
         exhausted),

        ("high impact",
         {**base, "family": "F2", "use_case": "payout"},
         RESOURCES),

        ("unknown capability",
         {**base, "family": "UNKNOWN"},
         RESOURCES),
    ]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", help="show only the named scenario")
    args = parser.parse_args()
    found = False
    for name, request, resources in scenarios():
        if args.scenario and name != args.scenario:
            continue
        found = True
        print(json.dumps({"scenario": name, "nature": "simulation", "request": request,
                          "result": choose(request, resources)}))
    if not found:
        parser.error("unknown scenario")


if __name__ == "__main__":
    main()
