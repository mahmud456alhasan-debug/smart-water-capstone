# Smart Water Lab — Wiki Home

Copy this page into **GitHub → Wiki → Create first page**.

---

## Overview

**Smart Water Lab** is an AI-augmented water resources decision support platform developed for the course *AI-Augmented Software Engineering* (XJTU, 2026).

**Student:** Mahmudul Hasan (4125999049)

## Integrated pipeline

1. **Rainfall monitoring** — OpenWeather API, forecast risk, alerts  
2. **Runoff estimation** — SCS-CN with uncertainty band  
3. **Reservoir dispatch** — optimization + Monte Carlo  
4. **Flood impact** — DEM inundation mapping  

See root README pipeline figure: `assets/smart_water_pipeline.png`

## Reports (PDF)

| Experiment | PDF path in repo |
|------------|------------------|
| Case study | `portfolio/AI_Engineering_Portfolio.pdf` |
| Exp 1 | `experiment1/` |
| Exp 2 | `experiment2/` |
| Exp 3 | `experiment3/` |
| Exp 4 | `experiment4/` |

## Verification

- **88 pytest** cases across four experiments  
- **4 validation CLIs**  
- **Swiss Cheese** layered checks documented in case study  
- **9 AI corrections** logged with human verification  

## Capstone

```bash
streamlit run app/main.py
pytest -q
```

## Wiki pages to add

- Experiment 1 — Rainfall Alert  
- Experiment 2 — SCS-CN Runoff  
- Experiment 3 — Reservoir Optimization  
- Experiment 4 — Flood Inundation  
- AI Engineering Portfolio  

Each page can link to the corresponding PDF and `submission/.../screenshots/` folder.
