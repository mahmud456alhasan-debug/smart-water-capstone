# Capstone Scope — Smart Water Integrated Dashboard

**Student:** Mahmudul Hasan (4125999049)  
**Course:** AI-Augmented Software Engineering (Week 7 Session A)

## Project title

Smart Water Integrated Monitoring and Decision Support Dashboard

## Problem statement

Urban and watershed managers need one place to connect rainfall observations, estimated runoff, reservoir release trade-offs, and flood extent under a chosen water level. In Weeks 3--6 this work lived in separate Python scripts. The capstone unifies those modules in a single Streamlit application with reproducible sample data, physical sanity checks, and documented AI-assisted development (`AGENTS.md`, `prompt_log.md`).

## Target users

- Hydrology / water-resources students practicing AI-assisted development  
- Municipal flood-duty staff reviewing thresholds and maps (demo / training, not operations)  
- Researchers prototyping integrated screening workflows before GIS production tools  

## Functional requirements

1. **Weather / alerts:** Load rainfall from CSV or optional API; show threshold-based alert status (from Week 5 Lab 1 pattern).  
2. **Runoff:** Compute SCS-CN runoff for sample storms; enforce runoff ≤ rainfall (Week 3 / Week 5 Lab 2).  
3. **Reservoir:** Run 7-day dispatch optimization summary (Week 6 Lab 3; MCM storage, m³/s flows).  
4. **Flood map:** Inundation from synthetic DEM + `flood_level` (Week 6 Lab 4).  
5. **Navigation:** Streamlit multi-tab UI linking the four modules with consistent units in labels.  

## Non-functional requirements

- Python 3.8+; install via `requirements.txt`  
- Runs offline on bundled sample data (fixed seeds)  
- Documented units (mm, m³/s, MCM, m) in UI and README  
- `prompt_log.md` maintained for all major AI prompts (Week 7--8)  
- Modular `src/` packages reusable from prior `ai_water_lab` labs  

## Success criteria

- End-to-end demo on sample data without editing source before run  
- At least one automated test for hydrologic validity (e.g. runoff ≤ rainfall)  
- Public GitHub repository with README, `AGENTS.md`, and planning artifacts from Session A  
- Live Streamlit demo acceptable on local host for Week 8 presentation  

## Scope boundaries (out of scope)

- Production deployment on Vercel / Streamlit Cloud (optional stretch)  
- Real-time national GIS or licensed DEM tiles (synthetic DEM only for capstone)  
- Multi-reservoir network or stochastic optimization  
- SMS / email alert delivery in production  

## Prior lab reuse

| Module | Source folder |
|--------|----------------|
| Weather / alerts | `week5_session_a_lab1/` |
| SCS-CN runoff | `week5_session_b_lab2/`, `week3_session_b/` |
| Reservoir dispatch | `week6_session_a_lab3/` |
| Flood inundation | `week6_session_b_lab4/` |
