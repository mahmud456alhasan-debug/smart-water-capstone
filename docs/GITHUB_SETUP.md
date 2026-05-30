# GitHub repository setup

Complete these on [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone) after pushing the latest README and `assets/`.

---

## 1. About section (gear icon on repo home)

**Description**

```
AI-Augmented Smart Water Lab: rainfall monitoring, runoff modeling, reservoir optimization, flood analysis, 88 tests, 5 PDF reports, AI engineering case study.
```

**Topics** (add all that fit)

```
python
hydrology
water-resources
streamlit
optimization
flood-modeling
reservoir-optimization
scipy
pytest
ai-engineering
decision-support
```

---

## 2. Push latest presentation changes

```bash
cd ~/Downloads/Software\ Development/ai_water_lab/capstone
git add README.md assets/ docs/ .gitignore
git commit -m "Engineering showcase README, assets gallery, docs"
git push origin main
```

If commit fails with a hook error, use:

```bash
git commit -F /tmp/commitmsg.txt
# where commitmsg.txt contains one line: Engineering showcase README, assets gallery, docs
```

---

## 3. Create Release v1.0 — Course Submission

**GitHub → Releases → Draft a new release**

| Field | Value |
|-------|--------|
| Tag | `v1.0.0` |
| Title | `v1.0 — Course Submission` |
| Description | See below |

**Attach files** (upload from `submission/`):

- `submission/portfolio/AI_Engineering_Portfolio.pdf`
- `submission/experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf`
- `submission/experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf`
- `submission/experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf`
- `submission/experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf`

**Release notes template:**

```markdown
## Smart Water Lab v1.0 — Course Submission

- 4 specialized hydrology experiments + capstone dashboard
- AI-Augmented Engineering Case Study (PDF)
- 88 automated tests, 4 validation CLIs
- Monte Carlo reservoir uncertainty, forecast risk pipeline
- Integrated pipeline and maturity figures in README

Mahmudul Hasan (4125999049) — Xi'an Jiaotong University — 2026
```

### CLI (if `gh` is authenticated)

```bash
cd capstone
gh release create v1.0.0 \
  --title "v1.0 — Course Submission" \
  --notes-file docs/RELEASE_NOTES.md \
  submission/portfolio/AI_Engineering_Portfolio.pdf \
  submission/experiment_reports/Experiment1_Rainfall_Alert/Experiment1_Rainfall_Alert_Report.pdf \
  submission/experiment_reports/Experiment2_SCSCN_Runoff/Experiment2_SCSCN_Runoff_Report.pdf \
  submission/experiment_reports/Experiment3_Reservoir_Optimization/Experiment3_Reservoir_Optimization_Report.pdf \
  submission/experiment_reports/Experiment4_Flood_Inundation/Experiment4_Flood_Inundation_Report.pdf
```

---

## 4. Enable Wiki (optional, ~15 min)

1. Repo **Settings → Features → Wikis → check ON**  
2. **Wiki → Create first page** — paste content from `docs/WIKI_HOME.md`  
3. Add pages for Experiments 1–4 linking to PDFs  

---

## 5. GitHub Pages (optional, Tier 4)

Not required for grading. If desired later:

- Settings → Pages → Source: branch `main`, folder `/docs`  
- Add `docs/index.md` landing page (future work)

---

## Checklist

- [ ] About description + topics set  
- [ ] README shows pipeline + radar images on first scroll  
- [ ] No `__pycache__` or `.coverage` in file tree  
- [ ] Release v1.0 with 5 PDFs attached  
- [ ] Wiki home page (optional)
