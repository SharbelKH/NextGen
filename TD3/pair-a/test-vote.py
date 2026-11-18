#!/usr/bin/env python3
"""Contract tests of Orchestrateur.vote_k_sur_n (TD 2, Pair A). No network, no key.

    python test-vote.py      # prints one line per test, exit code 1 if any test fails
"""
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location("skeleton", Path(__file__).with_name("skeleton-multi-llm-en.py"))
skeleton = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = skeleton
spec.loader.exec_module(skeleton)
vote = lambda proposals, k: skeleton.Orchestrateur.vote_k_sur_n(None, proposals, k)

A = ("groq", "openai/gpt-oss-120b")
B = ("openrouter", "cohere/north-mini-code:free")
C = ("groq", "qwen/qwen3.8-27b")
D = ("groq", "openai/gpt-oss-20b")
E = ("openrouter", "dots-studio/dots-3-note-preview:free")


def p(member, value):
    return SimpleNamespace(provider=member[0], model_requested=member[1], value=value,
                           verdict="executed" if value is not None else "error")


def raises(proposals, k):
    try:
        vote(proposals, k)
    except ValueError as exc:
        return str(exc)
    return None


TESTS = [
    ("agreement 2-of-3", lambda: vote([p(A, 100), p(B, 100), p(C, 120)], 2),
     {"consensus": True, "value": 100, "votes": 2}),
    ("disagreement 2-of-3 abstains", lambda: vote([p(A, 100), p(B, 110), p(C, 120)], 2),
     {"consensus": False, "value": None, "votes": 1}),
    ("one unavailable stays in n: 2 votes of 3 still pass", lambda: vote([p(A, 100), p(B, None), p(C, 100)], 2),
     {"consensus": True, "value": 100, "votes": 2}),
    ("two unavailable: 1 vote of n=3 abstains", lambda: vote([p(A, 100), p(B, None), p(C, None)], 2),
     {"consensus": False, "value": None, "votes": 1}),
    ("all unavailable: 0 votes, abstains", lambda: vote([p(A, None), p(B, None), p(C, None)], 2),
     {"consensus": False, "value": None, "votes": 0}),
    ("wrong consensus is kept (the vote never sees the reference)", lambda: vote([p(A, 0), p(B, 0), p(C, 100)], 2),
     {"consensus": True, "value": 0, "votes": 2}),
    ("3-of-5: 3 equal values pass", lambda: vote([p(A, 5), p(B, 5), p(C, 7), p(D, 5), p(E, None)], 3),
     {"consensus": True, "value": 5, "votes": 3}),
    ("3-of-5: 2-2-1 abstains", lambda: vote([p(A, 5), p(B, 7), p(C, 7), p(D, 5), p(E, 9)], 3),
     {"consensus": False, "value": None, "votes": 2}),
    ("3-of-5: two unavailable stay in n, 2 votes abstain", lambda: vote([p(A, 5), p(B, None), p(C, 5), p(D, None), p(E, 9)], 3),
     {"consensus": False, "value": None, "votes": 2}),
    ("duplicate provider:model refused", lambda: raises([p(A, 100), p(A, 100), p(C, 120)], 2), "duplicate"),
    ("k not a strict majority refused (k=1, n=3)", lambda: raises([p(A, 1), p(B, 1), p(C, 1)], 1), "strict majority"),
    ("k greater than n refused (k=4, n=3)", lambda: raises([p(A, 1), p(B, 1), p(C, 1)], 4), "strict majority"),
    ("k = n/2 refused for even n (k=2, n=4)", lambda: raises([p(A, 1), p(B, 1), p(C, 2), p(D, 2)], 2), "strict majority"),
]

failed = 0
for name, run, expected in TESTS:
    result = run()
    if isinstance(expected, dict):
        ok = isinstance(result, dict) and all(result.get(key) == value for key, value in expected.items())
    else:
        ok = isinstance(result, str) and expected in result
    failed += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {name}: {result}")
print(f"\n{len(TESTS) - failed}/{len(TESTS)} tests passed")
sys.exit(1 if failed else 0)
