#!/usr/bin/env python3
"""Spot-check reference cases for prompt_log / Exercise 3."""

from src.runoff import calculate_runoff

CASES = [
    (50, 80, 13.80),
    (80, 85, 43.55),
    (10, 80, 0.0),
    (50, 100, 50.0),
]

if __name__ == "__main__":
    for p, cn, expected in CASES:
        q = calculate_runoff(p, cn)
        ok = abs(q - expected) < 0.1 or (expected == 0 and q == 0)
        print(f"P={p} CN={cn} -> Q={q:.2f} (expect ~{expected}) {'OK' if ok else 'CHECK'}")
