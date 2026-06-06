# AGENTS.md — Experiment 4: Flood Inundation (DEM)

**Student:** Mahmudul Hasan (4125999049)

## Experiment goal

Bathtub inundation on a synthetic 100×100 DEM: flooded mask, depth, area %, volume vs water level; maps, curves, validation, seed sensitivity.

## Physical constraints

| Rule | Enforcement |
|------|-------------|
| Depth ≥ 0 | max(0, level − elevation) |
| Flooded ⇔ elev < level | Strict `<` documented |
| Area % monotonic in level | Validation checklist |
| Volume monotonic in level | Volume curve + pytest |
| Cell size 1 m | Area and volume in m²/m³ |

## Known assumptions

- Flat water surface (no routing).
- DEM seed 42 for main results; seeds 7/99 for sensitivity.
- Levels 40 m and 50 m are guide reference cases.

## Testing strategy

1. **pytest** — core flood math, curve monotonicity, scientific outputs (22 tests).
2. **validate_flood.py** — 9-point physical checklist → `validation_report.txt`.
3. **Seed sensitivity** — `sensitivity_seeds.csv`.
4. **Animation** — `flood_rise_animation.gif` with level/%/volume overlay.

## Validation rules (Swiss Cheese)

| Layer | Check |
|-------|--------|
| AI-generated mask logic | Manual review of `<` vs `≤` |
| Unit tests | 22 passed |
| validate_flood.py | 9/9 PASS |
| Monotonic curves | Area and volume vs stage |
| Seed robustness | ~25% at 50 m across seeds |

## Run commands

```bash
cd experiment4_flood_inundation
pip install -r requirements.txt
python3 main.py
python3 validate_flood.py
pytest -v
python3 generate_report_figures.py
```

## AI collaboration

AI may omit `max(0,·)` on depth or confuse stage vs depth-above-channel. Cross-check with `validate_flood.py`. Log in `prompt_log.md`.
