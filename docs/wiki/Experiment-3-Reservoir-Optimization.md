# Experiment 3 — Reservoir Optimization

## Purpose

Operational decision stage — 7-day hydropower dispatch under storage and ecological constraints.

## Capabilities

- Joint optimization (`trust-constr` + SLSQP cross-check)
- Ecological release trade-off sweep
- Drought / normal / wet scenario comparison
- **Monte Carlo** inflow uncertainty (100 scenarios, P10/P50/P90)
- `validate_constraints.py` — constraint audit CLI

## Report

[Experiment3_Reservoir_Optimization.pdf](../../release/Experiment3_Reservoir_Optimization.pdf)

## Key results

- Baseline revenue ~$146,443 (H=80 m, 7-day horizon)
- Drought scenario may be **infeasible** at Q_eco=10 — reported honestly

## Role in pipeline

Defines release schedules and downstream flow context for Experiment 4 flood assessment.
