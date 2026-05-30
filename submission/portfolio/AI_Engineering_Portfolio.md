# AI-Augmented Engineering Case Study for Smart Water Systems

**Student:** Mahmudul Hasan (4125999049)  
**Course:** AI-Augmented Software Engineering (XJTU, 2026)

This document reframes the Smart Water Lab suite as a **research-grade engineering case study**: integrated hydrology workflow, critical AI use with measured corrections, reproducibility scorecards, and explicit threats to validity—not a checklist of homework scripts.

*Companion figures:* `smart_water_pipeline.png`, `case_study_radar.png` (generate via `ai_water_lab/generate_case_study_figures.py`).

---

## 1. Integrated system architecture

Four experiments compose one **Smart Water Decision Support Pipeline**:

| Stage | Experiment | Role |
|-------|------------|------|
| Input | Weather / forecast | OpenWeather current + 3h/6h forecast rates |
| Monitor | Exp 1 — Rainfall alert | Threshold classification + forecast risk |
| Transform | Exp 2 — SCS-CN runoff | Event runoff Q(P, CN) + CN uncertainty band |
| Operate | Exp 3 — Reservoir optimization | 7-day dispatch + Monte Carlo inflow risk |
| Impact | Exp 4 — Flood inundation | Stage–area–volume curves on synthetic DEM |
| Integrate | Capstone (optional) | Streamlit dashboard wiring all modules |

See `ai_water_lab/SMART_WATER_PIPELINE.md` and **`smart_water_pipeline.png`**.

---

## 2. AI collaboration statistics

### Errors caught by experiment

| Experiment | AI errors found | Primary error types |
|------------|----------------:|---------------------|
| Exp 1 — Rainfall | 3 | API field handling, credential storage, dry-city logic |
| Exp 2 — SCS-CN | 2 | Formula typo (`25400/CN−254`), Q > P edge case |
| Exp 3 — Reservoir | 2 | Optimizer infeasibility, trade-off bound misuse |
| Exp 4 — Flood | 2 | Depth convention, monotonicity evidence |
| **Total** | **9** | Documented in challenged-output table below |

### Prompt / output summary (Experiments 1–4)

| Metric | Count | Notes |
|--------|------:|-------|
| Major AI-generated deliverables reviewed | 52 | Modules, reports, figures, validation CLIs |
| Accepted without material correction | 43 | Scaffold, tests, README, report structure |
| Required human correction | 9 | All logged in `prompt_log.md` + Section 3 |
| **Effective first-pass rate** | **83%** | Corrections caught before submission |

*Method:* Count discrete AI outputs (files or report sections) that underwent human review; “correction” = physics, API, or constraint fix documented in prompt logs or validation.

This demonstrates **critical AI use**—not blind acceptance.

---

## 3. AI outputs challenged (master evidence table)

| Experiment | AI suggestion | Problem found | Human verification | Final fix |
|------------|---------------|---------------|-------------------|-----------|
| **1 Rainfall** | Fetch rainfall; raise if no `rain` field | Dry cities would error | 50-city JSON + pytest | Missing `rain` → 0 mm/h |
| **1 Rainfall** | Hardcode API key | Security risk | Code review | Env var only |
| **1 Rainfall** | Current weather only | Title says “forecasting” | Forecast API review | `forecast_engine.py` 3h/6h pipeline |
| **2 SCS-CN** | SCS formula in code | Wrong S variant | Hand calc → 13.80 mm | Correct division form |
| **2 SCS-CN** | Return Q from formula | Q > P possible | Parametrized grid | `min(Q,P)` cap |
| **3 Reservoir** | SLSQP optimize | Infeasible storage | `validate_schedule()` | Feasible x₀ + trust-constr |
| **3 Reservoir** | Trade-off vs Q_eco | Fake feasible points | Hydrology review days 3–4 | Mark infeasible honestly |
| **4 Flood** | Depth = level − elev | Negative depth | Physical checklist | `max(0,·)`; strict `<` mask |
| **4 Flood** | Single flood map | No monotonicity proof | Rising curve + validate | 9/9 validation PASS |

---

## 4. Manual vs AI-assisted development benchmark

*Author estimates for comparable scope (single developer, familiar with Python/hydrology).*

| Task | Manual estimate | AI-assisted (actual) | Verification cost |
|------|----------------:|---------------------:|--------------------|
| Exp 1 — API + alerts + forecast | 4 h | ~45 min coding + 1 h review/tests | 1 h (pytest + 50-city run) |
| Exp 2 — SCS-CN + sensitivity + CN band | 6 h | ~1.5 h coding + 1 h review | 45 min (hand calc CLI) |
| Exp 3 — Optimization + trade-off + MC | 8 h | ~2 h coding + 2 h validation | 1.5 h (constraints + MC) |
| Exp 4 — DEM flood + scientific analysis | 6 h | ~1 h coding + 1.5 h review | 1 h (9-point checklist) |
| LaTeX reports + portfolio (×4) | 12 h | ~3 h AI draft + 4 h human edit | Cross-read all claims |
| **Total** | **~36 h** | **~18 h** | **~5 h verification** |

**Findings:** AI roughly **halved implementation time** on boilerplate and structure. **Verification cost remained ~25–30%** of total effort—consistent with the course Jagged Frontier model. Failures clustered on units, constraints, and physical edge cases, not syntax.

---

## 5. Reproducibility scorecards

| Item | Exp 1 | Exp 2 | Exp 3 | Exp 4 |
|------|:-----:|:-----:|:-----:|:-----:|
| README | ✓ | ✓ | ✓ | ✓ |
| AGENTS.md | ✓ | ✓ | ✓ | ✓ |
| prompt_log.md | ✓ | ✓ | ✓ | ✓ |
| pytest (green) | ✓ (20) | ✓ (23) | ✓ (23) | ✓ (22) |
| Validation script | ✓ | ✓ | ✓ | ✓ |
| Figures auto-generated | ✓ | ✓ | ✓ | ✓ |
| requirements.txt | ✓ | ✓ | ✓ | ✓ |
| audit_summary.txt | ✓ | ✓ | ✓ | ✓ |
| LaTeX report | ✓ | ✓ | ✓ | ✓ |

**Suite total:** 88 pytest cases; regenerate figures with `generate_report_figures.py` per experiment.

---

## 6. Threats to validity

| Threat | Impact | Mitigation in this work |
|--------|--------|-------------------------|
| OpenWeather availability & sparsity of `rain` fields | Forecast/monitor reliability varies by city | Demo mode; missing rain → 0 mm/h; 50-city batch logged |
| SCS-CN lumped assumptions | May not generalize to all watersheds / AMC states | CN uncertainty band [75, 85]; hand reference case |
| Simplified reservoir inflows | 7-day vector, not ensemble forecast | Monte Carlo perturbation; drought scenario infeasibility shown |
| Bathtub flood model | No routing, buildings, or hydrodynamics | Documented in `interpretation.md`; seed sensitivity |
| LLM hallucination risk | Wrong formulas or APIs | Swiss Cheese layers; 9 documented corrections |
| Self-assessed radar chart | Subjective maturity scores | Transparent 1–10 rubric; evidence in scorecards above |

---

## 7. Swiss Cheese Model (layered verification)

| Layer | Exp 1 | Exp 2 | Exp 3 | Exp 4 |
|-------|-------|-------|-------|-------|
| 1 — AI review | Env keys, forecast API | Formula vs NRCS | formulation.md first | `<` vs `≤` |
| 2 — pytest | 20 | 23 | 23 | 22 |
| 3 — Physical rules | Thresholds, rain ≥ 0 | Q ≤ P | Storage, eco, balance | Depth ≥ 0, monotonic |
| 4 — Validation CLI | 50-city + forecast | validate_reference | validate_constraints | validate_flood 9/9 |
| 5 — Report evidence | Terminal + PNGs | Hand calc + plots | Solver + MC histograms | Maps + curves |

---

## 8. Test inventory

| Experiment | Tests |
|------------|------:|
| Exp 1 — Rainfall alert | 20 |
| Exp 2 — SCS-CN runoff | 23 |
| Exp 3 — Reservoir optimization | 23 |
| Exp 4 — Flood inundation | 22 |
| **Total** | **88** |

```bash
for d in experiment1_rainfall_alert experiment2_scscn_runoff \
         experiment3_reservoir_optimization experiment4_flood_inundation; do
  (cd "ai_water_lab/$d" && pytest -q) || exit 1
done
```

---

## 9. Engineering maturity (self-assessment)

See **`case_study_radar.png`**: six axes (technical quality, testing, physical validation, AI collaboration, reproducibility, documentation) comparing a typical course project baseline to this submission.

---

## 10. Tools used

| Tool | Role | Limitation |
|------|------|------------|
| Cursor Agent | Primary implementation, tests, reports | Must run pytest locally |
| ChatGPT | Rubric, case-study framing, peer lens | Advisory; cross-check recommended |
| DeepSeek / Gemini / Kimi | Formula & syllabus cross-check | Not source of truth |

---

## 11. Submission checklist

- [ ] Four experiment PDFs compiled (Overleaf, twice each)
- [ ] This case study PDF compiled (`AI_Engineering_Portfolio.tex`)
- [ ] Pipeline + radar figures included
- [ ] All `pytest -q` green (88 tests)
- [ ] Cross-check with ChatGPT, DeepSeek, Gemini (course recommendation)

---

*Also published as LaTeX:* `AI_Engineering_Portfolio.tex` (compile to PDF for LMS).
