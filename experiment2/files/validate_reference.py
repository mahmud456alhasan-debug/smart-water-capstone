#!/usr/bin/env python3
"""Experiment 2 Part 4 - hand calculation and physical validation (CLI evidence)."""

from __future__ import annotations

import itertools

from scscn_runoff import calculate_Ia, calculate_S, calculate_runoff

CN_SENSITIVITY = [60, 70, 80, 90, 95, 100]
P_REF = 50.0
CN_REF = 80


def hand_calculation_demo() -> None:
    P, CN = P_REF, CN_REF
    S = calculate_S(CN)
    Ia = calculate_Ia(CN)
    Q = calculate_runoff(P, CN)
    print("=== Hand calculation (experiment guide) ===")
    print(f"P = {P} mm, CN = {CN}")
    print(f"S  = 25400/{CN} - 254 = {S:.4f} mm")
    print(f"Ia = 0.2 * S = {Ia:.4f} mm")
    print(f"Q  = ({P}-{Ia:.1f})^2 / ({P}-{Ia:.1f}+{S:.1f}) = {Q:.4f} mm")
    print(f"Check Q <= P: {Q:.4f} <= {P} -> {Q <= P}")
    print(f"Guide expected ~13.8 mm; code within 0.1 mm: {abs(Q - 13.8) < 0.1}")


def sensitivity_table() -> None:
    print("\n=== Sensitivity at P = 50 mm ===")
    print(f"{'CN':>4}  {'Q (mm)':>10}")
    for cn in CN_SENSITIVITY:
        print(f"{cn:4d}  {calculate_runoff(P_REF, cn):10.4f}")


def physical_validation_matrix() -> None:
    print("\n=== Physical validation matrix ===")
    checks = []
    # Q <= P grid sample
    ok_qp = all(
        calculate_runoff(float(p), float(cn)) <= float(p)
        for p, cn in itertools.product([0, 10, 50, 100], CN_SENSITIVITY)
    )
    checks.append(("Q <= P (sample grid)", "PASS" if ok_qp else "FAIL"))
    # P < Ia
    checks.append(
        ("P < Ia -> Q=0 (CN=80, P=10)", "PASS" if calculate_runoff(10, 80) == 0 else "FAIL")
    )
    # CN ordering
    qs = [calculate_runoff(P_REF, cn) for cn in CN_SENSITIVITY]
    checks.append(("Higher CN -> higher Q at P=50", "PASS" if qs == sorted(qs) else "FAIL"))
    checks.append(("CN=100 -> Q=P", "PASS" if calculate_runoff(50, 100) == 50 else "FAIL"))
    for name, status in checks:
        print(f"  {name}: {status}")


def main() -> None:
    hand_calculation_demo()
    sensitivity_table()
    physical_validation_matrix()
    print("\nAll domain checks complete.")


if __name__ == "__main__":
    main()
