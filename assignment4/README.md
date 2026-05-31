# Assignment 4 — Final Capstone Project

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026  
**Course:** AI-Augmented Software Engineering · **Weight:** 40% · **Due:** Week 16

---

## Project

**Smart Water Lab** — integrated rainfall monitoring, SCS-CN runoff, reservoir optimization, and flood inundation analysis in one Streamlit decision-support app.

**Repository:** https://github.com/mahmud456alhasan-debug/smart-water-capstone

---

## Submission package (this folder)

| File | Purpose |
|------|---------|
| [RUBRIC_MAPPING.md](RUBRIC_MAPPING.md) | Every rubric criterion → evidence link |
| [AI_FAILURES.md](AI_FAILURES.md) | All AI errors found and how they were caught |
| [FINAL_SUBMISSION_CHECKLIST.md](FINAL_SUBMISSION_CHECKLIST.md) | LMS / demo / GitHub checklist |
| [RUBRIC_MAPPING.pdf](RUBRIC_MAPPING.pdf) | PDF for upload (compile from `.tex`) |

---

## Required deliverables (Assignment 4)

**Assignment 4 is the whole repo** — code, tests, app, and docs. The `assignment4/` folder is only the rubric map and checklist.

| Requirement | Evidence (actual code/docs) |
|-------------|----------------------------|
| Functioning mini-app | [`../app/main.py`](../app/main.py) — `streamlit run app/main.py` |
| Test suite | [`../tests/`](../tests/) — **33** pytest cases |
| Physical validation | [`docs/PHYSICAL_VALIDATION.md`](../docs/PHYSICAL_VALIDATION.md) — 18 rules |
| AI failure table | [AI_FAILURES.md](AI_FAILURES.md) |
| 5-min presentation | [`docs/PRESENTATION_OUTLINE.md`](../docs/PRESENTATION_OUTLINE.md) — strict timing + tool comparison |
| AGENTS.md | [`../AGENTS.md`](../AGENTS.md) |
| Prompt log | [`../prompt_log.md`](../prompt_log.md) |
| Jagged Frontier | [`../docs/JAGGED_FRONTIER.md`](../docs/JAGGED_FRONTIER.md) |
| GitHub + README | [Repository](https://github.com/mahmud456alhasan-debug/smart-water-capstone) |
| Live demo (5 min) | [`../docs/DEMO_SCRIPT.md`](../docs/DEMO_SCRIPT.md) |
| Formal reports | [`../submission/`](../submission/) |
| Assignment 3 package | [`../assignment3/`](../assignment3/) |

---

## Quick run (for demo)

```bash
git clone https://github.com/mahmud456alhasan-debug/smart-water-capstone.git
cd smart-water-capstone
python3 -m pip install -r requirements.txt
streamlit run app/main.py
pytest -q
```

---

## What you must do manually

- [ ] **5-minute live presentation** — rehearse with `docs/DEMO_SCRIPT.md`  
- [ ] **LMS upload** — PDFs from `submission/`, `assignment3/`, `assignment4/`  
- [ ] **GitHub About + Release v1.0** — see [docs/GITHUB_SETUP.md](../docs/GITHUB_SETUP.md)
