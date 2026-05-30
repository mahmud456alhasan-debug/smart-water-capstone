# Smart Water Decision Support Pipeline

**Student:** Mahmudul Hasan (4125999049)

The four specialized experiments are not four isolated homework folders—they form a **single hydrology decision-support workflow** from weather observation to flood mapping.

## Integrated data flow

```
Weather & forecast data
        ↓
Rainfall alert + forecast risk (Exp 1)
        ↓
SCS-CN runoff + CN uncertainty (Exp 2)
        ↓
Reservoir optimization + Monte Carlo (Exp 3)
        ↓
Flood inundation mapping (Exp 4)
        ↓
Validation, audit summaries, LaTeX reports
        ↓
Capstone dashboard (optional integration)
```

## Module map

| Stage | Code folder | Primary outputs |
|-------|-------------|-----------------|
| Monitoring | `experiment1_rainfall_alert/` | `alert_log.txt`, forecast risk table |
| Runoff | `experiment2_scscn_runoff/` | Q(P, CN), `cn_uncertainty.csv` |
| Operations | `experiment3_reservoir_optimization/` | `optimal_schedule.csv`, `uncertainty_results.csv` |
| Impact | `experiment4_flood_inundation/` | Flood maps, volume curve, `validate_flood.py` |
| Integration | `capstone/` | Streamlit tabs wiring all four domains |

## Verification philosophy (suite-wide)

Every stage uses the same **Swiss Cheese** layers: AI review → pytest → physical rules → validation CLI → report evidence. See `../AI_Engineering_Portfolio.md` (case study).

## Generate pipeline figure

```bash
cd ai_water_lab
python3 generate_case_study_figures.py
```

Produces `smart_water_pipeline.png` and `case_study_radar.png`.
