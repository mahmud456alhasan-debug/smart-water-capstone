# Week 6 Session B Lab 4 -- Flood Inundation Analysis

**Student:** Mahmudul Hasan (4125999049)

## Model assumption

- `flood_level`: flat water surface elevation (m), same vertical datum as the DEM.
- Wet cells: `elevation <= flood_level`.
- Depth: `max(0, flood_level - elevation)` on wet cells; `0` elsewhere.
- Grid: 100x100 cells, **1 m** spacing (synthetic, no real CRS).

## Run (in order)

```bash
cd week6_session_b_lab4
python3 generate_dem.py
python3 run_flood_tests.py
python3 visualize_floods.py
python3 rising_water.py
```

## Outputs

| File | Exercise |
|------|----------|
| `data/dem.npy` | 1 |
| `figures/dem_heatmap.png` | 1 |
| `figures/flood_comparison_300dpi.png` | 3 |
| `figures/flooded_pct_vs_level.png` | 4 |
| `prompt_log.md` | submission |
