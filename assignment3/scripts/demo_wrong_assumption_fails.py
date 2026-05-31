#!/usr/bin/env python3
"""Assignment 3 demo: reproduce the Week 8 draft-test failure.

Simulates the AI-assisted wrong assertion:
  scs_runoff_mm(5.0, 95.0) == 0.0

Run from repo root:
  python3 assignment3/scripts/demo_wrong_assumption_fails.py

Expected exit code: 1 (AssertionError) — this IS the evidence of catching the mistake.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.runoff.scs_cn import scs_runoff_mm


def main() -> None:
    p, cn = 5.0, 95.0
    q = scs_runoff_mm(p, cn)
    print(f"SCS-CN: P={p} mm, CN={cn}")
    print(f"Computed Q = {q:.6f} mm")
    print()
    print("AI-assisted WRONG assumption: Q should be 0.0 for this case")
    print("Running: assert scs_runoff_mm(5.0, 95.0) == 0.0")
    assert q == 0.0, f"Expected 0 but got {q:.6f} mm — AI assumption was wrong"


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"\nAssertionError: {exc}")
        print("\nThis failure is the Assignment 3 evidence: test caught wrong AI reasoning.")
        sys.exit(1)
