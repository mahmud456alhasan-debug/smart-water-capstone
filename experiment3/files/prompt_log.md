# Prompt Log - Experiment 3: Reservoir Optimization

**Student:** Mahmudul Hasan (4125999049)
**Folder:** experiment3_reservoir_optimization/

---

## Part 1: Formulation (20%)

**Decision variables:** Q_t daily release (m^3/s), t=1..7.

**Unit convention:** Storage m^3; flows m^3/s; Vol = Q * 86400 s.

**Revenue model:** P = eta*rho*g*H*Q/1000 kW; E = P*24 kWh/day; R_t = p_t*E_t.
H = 80 m (stated); guide ~$45k uses H = 25-30 m (head sensitivity table).

**Multi-objective:** Hard eco floor via bounds; Pareto sweep Q_eco in {2,5,...,15} m^3/s.

**AI prompt (guide sample):**
Formulate 7-day reservoir dispatch with V_{t+1}=V_t+(I_t-Q_t)*86400,
maximize sum of price*energy, constraints on storage and Q_eco <= Q <= Q_max.

**Human edits:** Fixed max(Q_ECO, eco) bug; added feasible x0 forward pass.

---

## Part 2: Implementation (25%)

**Primary solver:** scipy.optimize.minimize, trust-constr, 7 variables, 14 inequalities.

**Cross-check:** compare_solvers() - SLSQP warm-started from trust-constr solution.

**Pedagogy:** optimize_day() with minimize_scalar.

**Tests:** test_reservoir_optimize.py - 18 pytest cases.

**CLI:** validate_constraints.py for report screenshot.

---

## Part 3: Trade-off Analysis (20%)

**Figure:** tradeoff_analysis.png (two panels).
**Data:** tradeoff_data.csv (11 eco scenarios).
**Insight:** Q_eco=10 baseline; Q_eco=11 costs ~$2,105; Q_eco>=12 infeasible.

---

## Part 4: Validation (10%)

**File:** validation_report.txt (7 sections).
**Checks:** All PASS; eco deficit 0.
**Revenue (H=80 m):** ~$146,443.
**Revenue (H=30 m, same Q):** ~$55k.

---

## Final polish

Key findings box, storage_bounds.png, infeasibility_explanation.png,
solver_comparison.csv, reproducibility section in LaTeX report.
