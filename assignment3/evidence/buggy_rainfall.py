"""
Week 2 Session A — Exercise 2: intentional bugs for CoT debugging practice.
Assignment 3 evidence: AI-style wrong SCS-CN formula.
"""

def calculate_runoff(P, CN):
    """Return runoff depth (mm) using SCS-CN — contains deliberate errors."""
    # Bug 1: should be 25400 / CN - 254
    S = 25400 * CN - 254

    # Bug 2: initial abstraction should be 0.2 * S, not 0.2 * P
    Ia = 0.2 * P

    # Bug 3: no early return when P < Ia (no runoff)

    # Bug 4: denominator should be (P - Ia + S), not (P + S)
    Q = (P - Ia) ** 2 / (P + S)

    return Q


if __name__ == "__main__":
    P = 80  # mm
    CN = 85
    Q = calculate_runoff(P, CN)
    print(f"Rainfall P = {P} mm, CN = {CN}")
    print(f"Computed runoff Q = {Q} mm")
