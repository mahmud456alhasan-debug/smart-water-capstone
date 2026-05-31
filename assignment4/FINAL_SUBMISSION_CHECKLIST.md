# Final Submission Checklist — Assignment 4

**Mahmudul Hasan (4125999049)**  
**Repo:** https://github.com/mahmud456alhasan-debug/smart-water-capstone

---

## GitHub (before LMS)

- [ ] **About** description + topics set ([docs/GITHUB_SETUP.md](../docs/GITHUB_SETUP.md))
- [ ] **Release v1.0** — 5 PDFs from `release/` attached
- [ ] **Tests badge** green (GitHub Actions)
- [ ] **Social preview** — `assets/smart_water_pipeline.png`

---

## LMS uploads

| File | Path |
|------|------|
| Assignment 3 — Swiss Cheese report | `assignment3/SWISS_CHEESE_REPORT.pdf` |
| Assignment 3 — Hallucination case study | `assignment3/HALLUCINATION_CASE_STUDY.pdf` |
| Assignment 4 — Rubric mapping | `assignment4/RUBRIC_MAPPING.pdf` |
| AI Engineering Portfolio | `submission/portfolio/AI_Engineering_Portfolio.pdf` |
| Experiment 1–4 reports | `submission/experiment_reports/*/…Report.pdf` |
| GitHub URL | https://github.com/mahmud456alhasan-debug/smart-water-capstone |

---

## Repo deliverables (already in tree)

- [x] `AGENTS.md`
- [x] `prompt_log.md`
- [x] `docs/JAGGED_FRONTIER.md`
- [x] `README.md` with quick start
- [x] `app/main.py` — Streamlit dashboard
- [x] `tests/` — **33** pytest cases ([docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md))
- [x] `src/validation.py` — physical rules
- [x] `assignment3/` — Swiss Cheese package
- [x] `assignment4/` — rubric mapping + AI failures

---

## Live demo (5 minutes — you)

- [ ] Rehearse with [docs/DEMO_SCRIPT.md](../docs/DEMO_SCRIPT.md)
- [ ] Time with [docs/PRESENTATION_OUTLINE.md](../docs/PRESENTATION_OUTLINE.md)
- [ ] Backup: Streamlit + pytest screenshots in `lab_reports/`
- [ ] App starts in < 30 s
- [ ] Copy `dem.npy` into `data/` for flood tab

---

## Defense talking points

1. **Problem:** four separate lab scripts → one integrated pipeline  
2. **Demo:** four Streamlit tabs (weather → runoff → reservoir → flood)  
3. **AI:** AGENTS.md + prompt log; **9 corrections** documented  
4. **Verification:** Swiss Cheese — **33** capstone tests + **88** experiment tests ([docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md))
5. **Jagged Frontier:** AI fast on scaffolding, weak on Ia/units/constraints  

---

## Regenerate assignment PDFs

```bash
cd assignment3 && pdflatex SWISS_CHEESE_REPORT.tex && pdflatex HALLUCINATION_CASE_STUDY.tex
cd ../assignment4 && pdflatex RUBRIC_MAPPING.tex && pdflatex RUBRIC_MAPPING.tex
```
