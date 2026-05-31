"""
Week 2 Session A — Exercise 2: corrected SCS-CN runoff calculation.
Assignment 3 evidence: fix after detecting AI-style bugs.
"""

def calculate_runoff(P, CN):
    """Return runoff depth (mm) using SCS-CN."""
    S = (25400 / CN) - 254
    Ia = 0.2 * S

    if P < Ia:
        return 0.0

    Q = (P - Ia) ** 2 / (P - Ia + S)
    return min(Q, P)


if __name__ == "__main__":
    P = 80  # mm
    CN = 85
    Q = calculate_runoff(P, CN)
    print(f"Rainfall P = {P} mm, CN = {CN}")
    print(f"Computed runoff Q = {Q:.1f} mm")
