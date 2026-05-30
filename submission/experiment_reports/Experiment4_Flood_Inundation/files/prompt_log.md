# Prompt Log - Experiment 4: Flood Inundation

**Student:** Mahmudul Hasan (4125999049)  
**Guide:** `experiment_guides/Experiment4_Flood_Inundation.md` (Week 6 Session B)

---

## Part 1: DEM

| Item | Value |
|------|--------|
| **Synthetic vs real DEM** | Synthetic 100x100 grid |
| **Random seed** | `np.random.default_rng(42)` |
| **Elevation range (min-max)** | 30.0 - 80.0 m (clipped) |
| **Cell size assumption** | 1 m x 1 m |
| **Curve step** | 0.5 m (21 points, 40--50 m) |
| **Terrain features** | Central valley, NW/SE hills, ridge, small noise |

**AI prompt (summary):** Generate synthetic DEM with valleys and hills; visualize heatmap; save `dem_data.npy`.

---

## Part 2: Flood logic

| Item | Value |
|------|--------|
| **Flood_level definition** | Absolute flat water-surface elevation (m), same datum as DEM |
| **Comparison operator** | Strict `<` (elevation below water surface) |
| **Depth** | `max(0, flood_level - elevation)` on wet cells; 0 elsewhere |

**Results at key levels:**

| Water level (m) | Flooded % | Mean depth wet (m) |
|-----------------|-----------|---------------------|
| 40 | 2.41 | 1.18 |
| 50 | 25.25 | 4.86 |

---

## Part 3-4: Figures

| File | Content |
|------|---------|
| `flood_extent_40m.png` | DEM + blue depth overlay at 40 m |
| `flood_extent_50m.png` | Same at 50 m |
| `flood_curve.png` | Water level vs flooded % (0.5 m step; min/max DEM reference lines) |
| `flood_percentages.csv` | Curve data export |
| `flood_comparison_40_50m.png` | Side-by-side (extra) |
| Flood volume at 40/50 m | Optional extension (m^3) |

**Monotonicity check:** `is_monotonic_non_decreasing()` on curve; asserted in `validate_physics()` and pytest.

---

## Part 5: Validation

| Check | Status |
|-------|--------|
| Flooded % increases with level | PASS (non-decreasing) |
| Max depth ~ level - min elevation | PASS |
| Percentage in [0, 100] | PASS |
| Water below min elev -> 0% | PASS |
| Water above max elev -> 100% | PASS |
| Units | Meters throughout |

**Edge cases tested:** Below `min(dem)-1`, above `max(dem)+1`, levels 40/45/50 m.

**Unexpected behavior:** None for bathtub model on smooth synthetic DEM.

## Scientific extensions (final polish)

| Item | Status |
|------|--------|
| DEM overview + contours | `dem_overview.png` |
| Elevation histogram @ 40/50 m | `dem_histogram.png` |
| Contour overlays on flood maps | Yes |
| Annotated flood curve | first flood, 10%, steepest growth |
| Flood volume curve | `flood_volume_curve.png` |
| Seed sensitivity (42, 7, 99) | `sensitivity_seeds.csv` |
| Performance benchmark | In `validation_report.txt` |
| Interpretation + limitations | `interpretation.md` + report |
| pytest | 21 passed |

---

## AI tools used

- Cursor agent for implementation aligned with Experiments 1-3 structure
- Cross-check research plans with ChatGPT, DeepSeek, and Gemini per course guidance
