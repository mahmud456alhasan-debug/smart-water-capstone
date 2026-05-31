#!/usr/bin/env python3
"""Compare legacy vs refactored stdout (Exercise 3).

Usage:
  python3 legacy_hydrology.py data/events.csv > legacy_out.txt
  python3 hydrology_modern.py data/events.csv > modern_out.txt
  python3 compare_outputs.py legacy_out.txt modern_out.txt
"""

import sys


def load(path):
    with open(path) as f:
        return [line.rstrip() for line in f if line.strip()]


def main():
    if len(sys.argv) != 3:
        print("Usage: compare_outputs.py legacy_out.txt modern_out.txt")
        sys.exit(1)
    a, b = load(sys.argv[1]), load(sys.argv[2])
    if a == b:
        print("MATCH: outputs identical line-by-line")
        sys.exit(0)
    print("DIFF: outputs differ")
    for i, (la, lb) in enumerate(zip(a, b)):
        if la != lb:
            print(f"  line {i+1} legacy: {la}")
            print(f"  line {i+1} modern: {lb}")
    if len(a) != len(b):
        print(f"  line counts: legacy={len(a)} modern={len(b)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
