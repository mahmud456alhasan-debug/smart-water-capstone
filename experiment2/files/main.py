#!/usr/bin/env python3
"""CLI entry: reference validation + quick runoff examples."""

import sys

from scscn_runoff import calculate_runoff

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        p, cn = float(sys.argv[1]), float(sys.argv[2])
        print(f"calculate_runoff({p}, {cn}) = {calculate_runoff(p, cn):.4f} mm")
    else:
        from validate_reference import main as validate_main

        validate_main()
