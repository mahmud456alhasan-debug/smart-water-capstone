# Week 6 Session A Lab 3 — Water Resources Optimization

**Student:** Mahmudul Hasan (4125999049)

## Unit convention (required by lab guide)

| Quantity | Units in code |
|----------|----------------|
| Storage `S` | MCM |
| Inflow / release rates | m³/s (inputs) |
| Daily volumes | MCM/day |

**Conversion:** `volume_mcm = flow_m3s * 86400 / 1e6` → factor **0.0864** MCM per (m³/s) per day.

**Water balance (one day):**

`S[t+1] = S[t] + inflow_volume_mcm - release_volume_mcm`

## Revenue model

- Head = 80 m, efficiency = 0.85 (constants in `reservoir_optimizer.py`)
- Power (MW) ≈ `HEAD * ETA * 9.81e-3 * Q_release` (m³/s)
- Energy (MWh/day) = Power × 24
- Revenue ($) = `price[$/MWh] * energy_MWh`

## Decision variable

Single release `Q` (m³/s) per day, optimized with `scipy.optimize.minimize_scalar` on bounds `[eco_min, Q_MAX]`.
