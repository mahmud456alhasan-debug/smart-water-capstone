#!/usr/bin/env python3
"""Part 4: standalone validation CLI (report evidence)."""

from reservoir_optimize import (
    HEAD_M,
    Q_ECO,
    compare_solvers,
    run_pipeline,
    solve_schedule,
    total_revenue_for_releases,
    validate_schedule,
    results_from_releases,
    head_sensitivity_table,
)


def main() -> None:
    print("=" * 72)
    print("Experiment 3 - Constraint validation CLI")
    print("=" * 72)

    results, total, check = run_pipeline()
    print(f"\nPrimary solver (trust-constr): revenue ${total:,.2f}, validation {check['ok']}")

    releases, _, _ = solve_schedule()
    print("\nHead sensitivity (same releases):")
    for h, rev in head_sensitivity_table(releases):
        print(f"  H = {h:5.1f} m  ->  ${rev:,.2f}")

    print("\nSolver comparison:")
    for name, info in compare_solvers().items():
        print(
            f"  {name}: revenue=${info['revenue_usd']:,.2f}, "
            f"feasible={info['feasible']}, {info['time_ms']:.1f} ms"
        )

    _, rev_11, _ = solve_schedule(eco_flow_m3s=11.0)
    eco_cost_11 = total - rev_11
    print(f"\nRevenue at Q_eco = 11 m^3/s (still feasible): ${rev_11:,.2f}")
    print(f"Cost of raising eco floor from 10 to 11 m^3/s: ${eco_cost_11:,.2f}")
    print("Revenue at Q_eco < 10 can look higher but violates the stated eco policy.")

    print(f"\nWrote validation_report.txt, optimal_schedule.csv (H={HEAD_M} m)")


if __name__ == "__main__":
    main()
