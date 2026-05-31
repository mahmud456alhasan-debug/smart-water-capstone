# System Architecture

Integrated Smart Water Decision Support Pipeline.

![Pipeline](../../assets/smart_water_pipeline.png)

## Workflow

```text
Weather data → Rainfall alert → SCS-CN runoff → Reservoir dispatch → Flood inundation mapping
```

| Stage | Module | Output |
|-------|--------|--------|
| 1 | Rainfall monitoring (Exp 1) | GREEN/YELLOW/RED alerts, forecast risk |
| 2 | Runoff modeling (Exp 2) | SCS-CN discharge, CN sensitivity |
| 3 | Reservoir optimization (Exp 3) | Dispatch schedule, eco/revenue trade-off |
| 4 | Flood analysis (Exp 4) | Inundation extent from DEM |

## Capstone integration

The Streamlit dashboard (`app/main.py`) combines all four modules with shared `src/` packages.

## Related

- [Home](Home.md)
- [Validation Strategy](Validation-Strategy.md)
- [Experiment Overview](Home.md#quick-links)
