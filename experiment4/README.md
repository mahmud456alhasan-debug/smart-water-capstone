# Experiment 4 — Flood Inundation Analysis

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

| Resource | Link |
|----------|------|
| **Report (PDF)** | [Experiment4_Flood_Inundation_Report.pdf](Experiment4_Flood_Inundation_Report.pdf) |
| **LaTeX source** | [Experiment4_Flood_Inundation_Report.tex](Experiment4_Flood_Inundation_Report.tex) |
| Appendix code | [`files/`](files/) |
| Figures | [`screenshots/`](screenshots/) |

Integrated in capstone: [`src/flood/`](../src/flood/)

Physical validation: **9/9** checks passed (bathtub model)

## Features

| Feature | Status |
|---------|--------|
| Synthetic 100×100 DEM, flood mask, depth, area % | Required |
| Maps at 40 m & 50 m, flood curve 40–50 m (0.5 m steps) | Required |
| Physical validation checklist (`validate_flood.py`) | Required |
| Flood volume curve + seed sensitivity | Extra |
| Rising-water GIF with volume overlay | Extra |
| Edge-seeded flood routing (4-neighbor BFS) | Extra |
| Building footprints as flood barriers | Extra |
| Bathtub vs routed comparison plot | Extra |
| **Real DEM loader (`.asc` / resampled `.npy`)** | Extra |
| pytest suite | Extra |

## Run locally

```bash
cd files
pip install -r requirements.txt
python flood_inundation.py          # all figures + GIF + validation report
python -m pytest -q                 # 40 tests
python validate_flood.py            # 9/9 physical checks
```

```bash
pdflatex Experiment4_Flood_Inundation_Report.tex && pdflatex Experiment4_Flood_Inundation_Report.tex
```
