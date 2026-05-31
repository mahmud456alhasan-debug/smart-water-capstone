# GitHub repository setup

Do these steps on [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone) after `git push`.

---

## Step 1 — About section (highest impact, 2 minutes)

On the repo home page, click the **gear icon** next to "About".

**Description** (paste exactly):

```
AI-Augmented Water Resources Decision Support Platform integrating rainfall monitoring, runoff modeling, reservoir optimization, flood-risk analysis, and engineering validation.
```

**Topics** (add each):

```
python
streamlit
hydrology
water-resources
optimization
monte-carlo
flood-modeling
rainfall-monitoring
scs-cn
reservoir-optimization
ai-engineering
software-engineering
decision-support
pytest
```

Save. The empty "No description" box disappears immediately.

---

## Step 2 — Push latest README

```bash
cd ~/Downloads/Software\ Development/ai_water_lab/capstone
git push origin main
```

---

## Step 3 — Create Release v1.0 (5 minutes)

**Releases → Draft a new release**

| Field | Value |
|-------|--------|
| Tag | `v1.0.0` (or `v1.0-course-submission`) |
| Release title | `v1.0 — Smart Water Lab Submission` |
| Description | Paste from `docs/RELEASE_NOTES.md` |

**Attach these 5 files** from the `release/` folder:

1. `AI_Engineering_Portfolio.pdf`
2. `Experiment1_Rainfall_Alert.pdf`
3. `Experiment2_SCSCN_Runoff.pdf`
4. `Experiment3_Reservoir_Optimization.pdf`
5. `Experiment4_Flood_Inundation.pdf`

Click **Publish release**. Visitors will see **Releases → v1.0** instead of "No releases published".

---

## Step 4 — Populate Wiki (optional, 15 minutes)

1. **Settings → General → Features → Wikis → ON**
2. Click **Wiki** tab → **Create the first page** — paste `docs/wiki/Home.md`
3. Create these pages (copy from matching files in `docs/wiki/`):

| Wiki page title | Source file |
|-----------------|-------------|
| Home | `Home.md` |
| System-Architecture | `System-Architecture.md` |
| Validation-Strategy | `Validation-Strategy.md` |
| Reproducibility-Guide | `Reproducibility-Guide.md` |
| AI-Engineering-Portfolio | `AI-Engineering-Portfolio.md` |
| Experiment-1-Rainfall-Alert | `Experiment-1-Rainfall-Alert.md` |
| Experiment-2-SCSCN-Runoff | `Experiment-2-SCSCN-Runoff.md` |
| Experiment-3-Reservoir-Optimization | `Experiment-3-Reservoir-Optimization.md` |
| Experiment-4-Flood-Inundation | `Experiment-4-Flood-Inundation.md` |

4. Set **Home** as the wiki start page (Wiki → Pages → Home → set as default if prompted)

---

## Step 5 — Verify landing page

After push, confirm README shows in order:

1. **Hero image** (pipeline architecture)
2. Title + one-paragraph summary
3. Shields.io badges
4. **Platform gallery** (2×2 screenshots)
5. **Results snapshot** (experiment outcomes table)
6. Key metrics
7. **Key deliverables** (PDF links + release)
8. **Learning journey** (Weeks 1–8 table + lab report preview)
9. Quick start
10. Repository structure
11. Further documentation links

Detailed engineering content lives in [`docs/ENGINEERING.md`](ENGINEERING.md), not the main README.

---

## Checklist

- [ ] About description + topics set
- [ ] `git push` complete
- [ ] Release v1.0 with 5 PDFs from `release/`
- [ ] Wiki home + experiment pages (optional)
- [ ] No `__pycache__` in file tree
