# AGENTS.md — Experiment 3: Reservoir Optimization

**Student:** Mahmudul Hasan (4125999049)

## Experiment goal

7-day joint reservoir dispatch: maximize hydropower revenue subject to storage bounds, mass balance, and ecological release floor Q_eco.

## Physical constraints

| Rule | Enforcement |
|------|-------------|
| V_min ≤ V_{t+1} ≤ V_max | NLP inequality constraints |
| Q_eco ≤ Q_t ≤ Q_max | Optimizer bounds |
| Mass balance | V_{t+1} = V_t + (I_t − Q_t)×86400 |
| Revenue | H = 80 m, η = 0.85, price $/kWh |

## Known assumptions

- Storage in m³; flows in m³/s; Δt = 86400 s.
- Guide inflow/price vectors fixed unless scenario mode used.
- Drought (−30% inflow) may be **infeasible** at Q_eco = 10 — report honestly.

## Testing strategy

1. **pytest** — balance, bounds, solvers, head table, validation file (20 tests).
2. **validate_constraints.py** — CLI evidence for report.
3. **tradeoff_analysis.py** — eco-flow sweep with infeasibility flags.
4. **scenario_analysis.py** — drought / normal / wet comparison.

## Validation rules (Swiss Cheese)

| Layer | Check |
|-------|--------|
| formulation.md | Human-written math before code |
| Feasible x₀ | Forward pass before trust-constr |
| pytest + validation CLI | All constraints PASS (baseline) |
| Trade-off sweep | Infeasible eco flagged, not faked |
| Scenario analysis | Drought infeasibility detected |

## Run commands

```bash
cd experiment3_reservoir_optimization
pip install -r requirements.txt
python3 main.py
python3 validate_constraints.py
pytest -v
python3 generate_report_figures.py
streamlit run reservoir_dashboard.py   # optional
```

## AI collaboration

AI often proposes SLSQP without feasible initial guess or wrong eco bound in trade-off sweeps. Always run `validate_constraints.py` after AI edits. Log in `prompt_log.md`.
