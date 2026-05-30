# Experiment 3 - Mathematical Formulation (Part 1)

**Student:** Mahmudul Hasan (4125999049)
**Folder:** experiment3_reservoir_optimization/

---

## 1. Decision variables

| Symbol | Meaning | Unit |
|--------|---------|------|
| Q_t    | Average reservoir release on day t | m^3/s |
| t      | Day index | 1..7 |

Vector form: Q = [Q_1, ..., Q_7]

---

## 2. Unit convention (experiment guide)

| Quantity | Symbol | Unit | Notes |
|----------|--------|------|-------|
| Storage | V | m^3 | State variable |
| Inflow / release | I_t, Q_t | m^3/s | Daily average |
| Timestep | dt | 86400 s | One day |
| Daily volume | Vol_t | m^3 | Vol_t = Q_t * dt |

Mass balance (consistent):

  V_{t+1} = V_t + (I_t - Q_t) * dt

Initial condition: V_0 = 500,000 m^3.

---

## 3. Parameters (experiment guide)

| Parameter | Value |
|-----------|-------|
| V_min, V_max | 100,000 / 1,000,000 m^3 |
| Q_max | 100 m^3/s |
| Q_eco (baseline policy) | 10 m^3/s |
| I_t | 15, 12, 10, 8, 12, 15, 18 m^3/s |
| p_t | 0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10 USD/kWh |

---

## 4. Revenue model (explicit assumption)

Nominal hydraulic head H = 80 m, efficiency eta = 0.85:

  P_t [kW] = eta * rho * g * H * Q_t / 1000
  rho = 1000 kg/m^3, g = 9.81 m/s^2

  E_t [kWh/day] = P_t * 24
  R_t [USD/day] = p_t * E_t

Objective: maximize sum_{t=1}^7 R_t  (minimize negative sum in scipy)

Guide reference (~$45k): peers using H = 25-30 m with the same Q report ~$46k-$55k.
Revenue magnitude is NOT a feasibility check; constraints are.

---

## 5. Multi-objective handling

- Weighted sum: not used
- Hard eco constraint: Q_t >= Q_eco_policy via bounds
- Pareto sweep: vary Q_eco_policy from 2 to 15 m^3/s

Ecological deficit (reporting): D = sum_t max(0, Q_eco_policy - Q_t)

---

## 6. Constraints

Release: Q_eco_policy <= Q_t <= Q_max
Storage: V_min <= V_{t+1}(Q) <= V_max
Mass balance: Section 2

Feasible release interval:
  Q_t <= I_t + (V_t - V_min) / dt
  Q_t >= I_t - (V_max - V_t) / dt
intersected with [Q_eco_policy, Q_max]

---

## 7-9. Implementation, trade-off, validation

See full formulation.md in code folder and validation_report.txt.
