# AGENTS.md -- Smart Water Capstone

## Project overview

Integrated Streamlit dashboard combining rainfall/alerts, SCS-CN runoff, reservoir dispatch (SciPy), and DEM-based flood inundation. Built from `ai_water_lab` Weeks 3--6. Student: Mahmudul Hasan (4125999049).

## Tech stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| Data | pandas, numpy |
| Optimization | scipy |
| Plots | matplotlib |
| Tests | pytest |
| Python | 3.8+ |

## Directory structure

```text
capstone/
  app/main.py
  src/weather/  src/runoff/  src/reservoir/  src/flood/
  data/  tests/
```

## Conventions

- Units: rainfall mm; reservoir storage MCM; flows m3/s; flood stage m (absolute, same as DEM).
- Reuse logic from week5/week6 labs; refactor into `src/` rather than copy-paste duplicates.
- Wet cell rule: `elevation <= flood_level`; depth zero off wet cells.
- Runoff must satisfy `Q <= P` where applicable.
- Commit messages: `Week N: short description`.
- Document every major AI prompt in `prompt_log.md`.

## Run commands

```bash
cd capstone
pip install -r requirements.txt
streamlit run app/main.py
pytest -q
```

## Week 7 Session B priorities

1. Wire `src/runoff` and `src/flood` with tests.  
2. Streamlit tabs with sample data.  
3. Integrate reservoir summary tab.  
4. Optional weather API behind env flag.
