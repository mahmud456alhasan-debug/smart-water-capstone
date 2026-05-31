# Engineering & Validation

Extended engineering evidence for the Smart Water Lab capstone. Summary metrics and gallery are on the [main README](../README.md).

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026

[← Back to repository](../README.md)

---

## Integrated system architecture

End-to-end decision-support workflow: **weather data → rainfall alert → SCS-CN runoff → reservoir dispatch → flood inundation mapping**, with validation and formal reports at each stage.

![Smart Water Decision Support Pipeline](../assets/smart_water_pipeline.png)

---

## Engineering outcomes

- **88** automated pytest cases across four experiments
- **4** dedicated validation CLI tools (`validate_*`, batch API, constraint checks)
- **5** formal PDF reports including AI engineering case study
- **Monte Carlo** inflow uncertainty — 100 scenarios, P10/P50/P90 revenue and storage
- **9** documented AI corrections (83% first-pass rate on 52 reviewed deliverables)
- **End-to-end pipeline** linking monitoring, operations, and flood impact assessment
- **4** reproducibility scorecards (`audit_summary.txt` per experiment)

---

## Engineering maturity

![Engineering maturity self-assessment](../assets/case_study_radar.png)

Six axes: technical quality, testing, physical validation, AI collaboration, reproducibility, documentation (1–10 self-assessment).

---

## Validation and AI engineering

| Layer | Implementation |
|-------|----------------|
| Swiss Cheese verification | AI review → pytest → physical rules → validation CLI → report evidence |
| Jagged Frontier | AI mistakes documented in `prompt_log.md` and case study |
| Critical AI use | 52 deliverables reviewed, 9 required human correction |
| Threats to validity | OpenWeather sparsity, SCS-CN lumped CN, bathtub flood model, LLM hallucination risk |

Full narrative: [submission/portfolio/AI_Engineering_Portfolio.md](../submission/portfolio/AI_Engineering_Portfolio.md) · Capstone reflection: [JAGGED_FRONTIER.md](../JAGGED_FRONTIER.md)

---

## Platform modules (detail)

| Module | Capabilities | Evidence |
|--------|--------------|----------|
| Rainfall (Exp 1) | OpenWeather API, GREEN/YELLOW/RED alerts, 3h/6h forecast | [Experiment 1 report](../submission/experiment_reports/Experiment1_Rainfall_Alert/) |
| Runoff (Exp 2) | SCS-CN, CN uncertainty bands, sensitivity | [Experiment 2 report](../submission/experiment_reports/Experiment2_SCSCN_Runoff/) |
| Reservoir (Exp 3) | trust-constr optimization, eco trade-off, Monte Carlo | [Experiment 3 report](../submission/experiment_reports/Experiment3_Reservoir_Optimization/) |
| Flood (Exp 4) | DEM inundation, level comparison, 9/9 validation PASS | [Experiment 4 report](../submission/experiment_reports/Experiment4_Flood_Inundation/) |

---

## Related

| Resource | Link |
|----------|------|
| Key deliverables (PDFs) | [README — Key deliverables](../README.md#key-deliverables) |
| Weekly lab progression | [lab_reports/README.md](../lab_reports/README.md) |
| Submission package | [submission/README.md](../submission/README.md) |
