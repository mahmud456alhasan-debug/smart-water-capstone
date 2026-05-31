# Prompt Log - Week 6 Session B Lab 4

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** Flood Inundation Analysis

---

## Flood_level definition used

**Absolute stage (m):** `flood_level` is the flat water surface elevation in the same datum as the DEM. A cell is wet when `elevation <= flood_level`. Depth is `max(0, flood_level - elevation)` on wet cells and `0` elsewhere.

---

## Cell size assumption

**1 m** square cells on a 100x100 synthetic grid (10,000 cells, 10,000 m^2 domain). Area statistics use cell count x 1 m^2 unless noted.

---

## Exercise 2 results (flood levels)

| Flood level (m) | Flooded % | Mean depth on wet (m) |
|-----------------|-----------|------------------------|
| 40 | 2.41 | 1.183 |
| 50 | 25.25 | 4.863 |
| 60 | 82.93 | 8.329 |

---

## Monotonicity check

**Status:** PASS

**Levels swept:** 40 to 60 m, step 1 m

**Figure:** `figures/flooded_pct_vs_level.png`

---

## Figure files

- `figures/dem_heatmap.png` -- Exercise 1 DEM
- `figures/flood_comparison_300dpi.png` -- Exercise 3 side-by-side (40, 50, 60 m)
- `figures/flooded_pct_vs_level.png` -- Exercise 4

---

## Lessons learned

Define wet/dry and depth conventions in `prompt_log.md` before plotting. A fixed random seed keeps DEM and submission figures reproducible. Rising-stage curves should be monotone non-decreasing; if not, check mask logic (`<=` vs `<`). This lab does not require OpenCode; local Python and the lab guide AI prompts are enough.
