# Assignment 4 — Final Capstone Project

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026  
**Course:** AI-Augmented Software Engineering · **Weight:** 40% · **Due:** Week 16

---

## Start here (for graders)

| Priority | File | Purpose |
|----------|------|---------|
| **1** | [README.md](README.md) | This page |
| **2** | [RUBRIC_MAPPING.pdf](RUBRIC_MAPPING.pdf) | Rubric → evidence (LMS) |
| **3** | [AI_FAILURES.pdf](AI_FAILURES.pdf) | AI mistakes table (LMS) |
| **4** | [app/](../app/) + [tests/](../tests/) | Working app + **33 pytest** |

**Optional:** [FINAL_SUBMISSION_CHECKLIST.pdf](FINAL_SUBMISSION_CHECKLIST.pdf) · formal reports in [submission/](../submission/) (5 PDFs)

---

## Project

**Smart Water Lab** — rainfall monitoring, SCS-CN runoff, reservoir optimization, flood analysis.

**Repository:** https://github.com/mahmud456alhasan-debug/smart-water-capstone

```bash
streamlit run app/main.py
pytest -q    # 33 passed (capstone repo)
```

---

## Required deliverables

| Requirement | Evidence |
|-------------|----------|
| Functioning mini-app | [`app/main.py`](../app/main.py) |
| Documentation | [`README.md`](../README.md) |
| AGENTS.md | [`AGENTS.md`](../AGENTS.md) |
| Prompt log | [`prompt_log.md`](../prompt_log.md) |
| Jagged Frontier | [`docs/JAGGED_FRONTIER.md`](../docs/JAGGED_FRONTIER.md) |
| Physical validation | [`docs/PHYSICAL_VALIDATION.md`](../docs/PHYSICAL_VALIDATION.md) |
| Live demo (5 min) | [`docs/PRESENTATION_OUTLINE.md`](../docs/PRESENTATION_OUTLINE.md) |
| Formal reports | [`submission/`](../submission/) |

**Honest note on AI use:** AI produced drafts for scaffold, tests, and docs; I verified, corrected, and tested all hydrology logic. Nine corrections documented in [AI_FAILURES.md](AI_FAILURES.md).

---

## All course assignments

| # | Folder |
|---|--------|
| 1 | [assignment1/](../assignment1/) |
| 2 | [assignment2/](../assignment2/) |
| 3 | [assignment3/](../assignment3/) |
| 4 | **this folder** + whole repo |

---

## Regenerate PDFs

```bash
cd assignment4
pdflatex RUBRIC_MAPPING.tex && pdflatex RUBRIC_MAPPING.tex
pdflatex AI_FAILURES.tex && pdflatex AI_FAILURES.tex
pdflatex FINAL_SUBMISSION_CHECKLIST.tex && pdflatex FINAL_SUBMISSION_CHECKLIST.tex
rm -f *.aux *.log *.out
```

---

## Manual steps remaining

- [ ] 5-minute live presentation (rehearse with timer)
- [ ] GitHub About + Release v1.0 — [docs/GITHUB_SETUP.md](../docs/GITHUB_SETUP.md)
- [ ] LMS upload
