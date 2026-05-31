# System Architecture -- Smart Water Capstone

## 1. Component diagram (logical)

```text
+------------------+     +------------------+
|  Weather / CSV   |---->|  Alert engine    |
+------------------+     +--------+---------+
                                  |
+------------------+     +--------v---------+
|  Rainfall series |---->|  SCS-CN runoff   |
+------------------+     +--------+---------+
                                  |
                         +--------v---------+
                         | Reservoir optim. |
                         +--------+---------+
                                  |
+------------------+     +--------v---------+
|  DEM (npy)       |---->| Flood inundation |
+------------------+     +--------+---------+
                                  |
                         +--------v---------+
                         | Streamlit UI     |
                         | (tabs / charts)  |
                         +------------------+
```

## 2. Directory structure

```text
capstone/
  README.md
  AGENTS.md
  requirements.txt
  prompt_log.md
  SCOPE.md
  ARCHITECTURE.md
  app/
    main.py                 # Streamlit entry, tab layout
  src/
    weather/                # load data, alert thresholds
    runoff/                 # SCS-CN, validation
    reservoir/              # horizon optimize, summary tables
    flood/                  # simulate_flood, plots
  data/
    sample_rainfall.csv
    dem.npy                 # copy or symlink from week6 lab
  tests/
    test_runoff.py
    test_flood.py
```

## 3. Module responsibilities

| Module | Responsibility |
|--------|----------------|
| `app/main.py` | Streamlit shell; sidebar settings; tab routing |
| `src/weather` | Parse CSV/API rainfall; compute alert level |
| `src/runoff` | SCS-CN Q(P, CN); clip Q when P < Ia |
| `src/reservoir` | Wrap `optimize_horizon`; display revenue / storage table |
| `src/flood` | `simulate_flood`, stats, matplotlib figures for UI |
| `tests/` | Physical checks and monotonic flood % |

## 4. Data flow

1. User selects storm CSV or default sample → rainfall depth mm.  
2. Runoff module returns Q mm; UI shows hydrograph or single-event Q.  
3. Optional: pass inflow series into reservoir module → 7-day schedule table.  
4. User sets `flood_level` (m) → flood module reads `data/dem.npy` → mask, depth, % flooded.  
5. Alert tab reads latest rainfall intensity vs configured thresholds.  

## 5. Technology stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.8+ |
| UI | Streamlit |
| Numerics | NumPy, Pandas |
| Optimization | SciPy (`minimize_scalar`) |
| Plotting | Matplotlib (embedded in Streamlit) |
| Tests | pytest |
| VCS | GitHub |
| AI workflow | Cursor / any LLM + `AGENTS.md` + `prompt_log.md` |

## 6. API design (internal Python, not REST)

| Function | Input | Output |
|----------|-------|--------|
| `load_rainfall_csv(path)` | file path | `DataFrame` datetime, mm |
| `compute_runoff(p_mm, cn)` | scalars/series | runoff mm |
| `run_reservoir_baseline()` | eco flow optional | schedule table, total revenue |
| `simulate_flood(dem, level)` | 2D array, float m | mask, depth |
| `evaluate_alerts(intensity_mm_h)` | float | GREEN / AMBER / RED |

External REST (OpenWeather) optional behind config flag; capstone defaults to CSV for reproducibility.
