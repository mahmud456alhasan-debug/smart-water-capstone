#!/usr/bin/env python3
"""Exercise 4: quick constraint validation printout."""

from reservoir_optimizer import ECO_FLOW_DEFAULT, optimize_horizon, validate_schedule


def main() -> None:
    results, total = optimize_horizon()
    check = validate_schedule(results, eco_flow_m3s=ECO_FLOW_DEFAULT)
    print(f"Total revenue: ${total:,.2f}")
    print("Validation:", "PASS" if check["ok"] else "FAIL")
    for v in check["violations"]:
        print(" ", v)
    if check["ok"]:
        print(f"  Min storage slack: {check['worst_storage_slack']:.3f} MCM")


if __name__ == "__main__":
    main()
