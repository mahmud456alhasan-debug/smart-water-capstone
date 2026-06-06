# AGENTS.md — Experiment 2: SCS-CN Runoff

**Student:** Mahmudul Hasan (4125999049)

## Experiment goal

Implement USDA SCS-CN direct runoff in tested Python code; validate hand calculation; produce sensitivity plots and physical constraint checks.

## Physical constraints

| Rule | Enforcement |
|------|-------------|
| Q ≥ 0 | Zero branch when P ≤ Ia |
| Q ≤ P | `min(Q, P)` after formula |
| CN ∈ (0, 100] | `ValueError` on bad CN |
| P ≥ 0 | `ValueError` on negative P |

## Known assumptions

- Metric units (mm); Ia = 0.2 S; S = 25400/CN − 254.
- Reference case: P = 50 mm, CN = 80 → Q = 13.80 mm.

## Testing strategy

1. **Guide cases** — P = 0, P < Ia, P = Ia, normal, CN = 100.
2. **Parametrized** — Q ≤ P on a P×CN grid.
3. **Hand validation** — `validate_reference.py` reproduces 13.80 mm.
4. **Sensitivity** — `sensitivity_analysis.py` → CSV + PNG.

## Validation rules (Swiss Cheese)

| Layer | Check |
|-------|--------|
| AI formula draft | Compared to NRCS handbook |
| pytest | 20 passed |
| Hand calc CLI | PASS at P=50, CN=80 |
| Physical grid | Q ≤ P all cells |
| Monotonic CN | Higher CN → higher Q at fixed P |

## Run commands

```bash
cd experiment2_scscn_runoff
pip install -r requirements.txt
pytest -v
python3 sensitivity_analysis.py
python3 validate_reference.py
python3 generate_report_figures.py
streamlit run runoff_explorer.py   # optional
```

## AI collaboration

Write tests before trusting AI-generated formulas. Log prompts in `prompt_log.md`.
