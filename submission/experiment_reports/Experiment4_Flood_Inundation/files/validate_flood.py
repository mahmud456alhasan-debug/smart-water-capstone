#!/usr/bin/env python3
"""Print validation checklist (for terminal screenshots)."""

from flood_inundation import load_dem, run_validation_checks, simulate_rising_water


def main() -> None:
    dem = load_dem()
    curve = simulate_rising_water(dem)
    checks = run_validation_checks(dem, curve)
    print("Experiment 4 - Physical validation")
    print("=" * 60)
    all_ok = True
    for c in checks:
        status = "PASS" if c.passed else "FAIL"
        if not c.passed:
            all_ok = False
        print(f"  [{status}] {c.name}")
        print(f"         {c.detail}")
    print("-" * 60)
    print(f"Overall: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
