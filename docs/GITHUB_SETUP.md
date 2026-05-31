# GitHub repository setup

What you can fix in code vs what only you can do on github.com.

| Task | Who | Time |
|------|-----|------|
| README, CI workflow, docs | **Already in repo** — push commits | — |
| **About** description + topics | **You — manual** | 30 sec |
| **Release v1.0** with 5 PDFs | **You — manual** | 5 min |
| **Social preview** image | **You — manual** | 1 min |
| Wiki pages | **You — optional** | 15 min |

---

## Step 1 — About section (YOU — manual, 30 seconds)

GitHub does **not** read description/topics from README. You must set them on the website.

1. Open [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone)
2. Click the **gear icon** next to **About** (right sidebar)
3. Paste **Description**:

```
AI-Augmented Water Resources Decision Support Platform integrating rainfall monitoring, runoff modeling, reservoir optimization, and flood-risk analysis.
```

4. Add **Topics** (one at a time):

```
python
streamlit
hydrology
water-resources
optimization
flood-modeling
monte-carlo
rainfall-monitoring
scs-cn
reservoir-optimization
software-engineering
ai-engineering
```

5. Click **Save changes**

---

## Step 2 — Push latest code (YOU — terminal)

```bash
cd ~/Downloads/Software\ Development/ai_water_lab/capstone
git push origin main
```

After push, the **Tests** badge in README will turn green once GitHub Actions runs (`.github/workflows/tests.yml`).

---

## Step 3 — Create Release v1.0 (YOU — manual, 5 minutes)

The README links to a release that does not exist until you create it.

1. **Releases** → **Draft a new release**
2. Fill in:

| Field | Value |
|-------|--------|
| Tag | `v1.0.0` |
| Release title | `v1.0 — Smart Water Lab Submission` |
| Description | Paste from [`RELEASE_NOTES.md`](RELEASE_NOTES.md) |

3. **Attach files** — drag from local `release/` folder:

- `AI_Engineering_Portfolio.pdf`
- `Experiment1_Rainfall_Alert.pdf`
- `Experiment2_SCSCN_Runoff.pdf`
- `Experiment3_Reservoir_Optimization.pdf`
- `Experiment4_Flood_Inundation.pdf`

4. **Publish release**

The sidebar will show **Releases → v1.0** instead of “No releases published”.

---

## Step 4 — Social preview image (YOU — manual, 1 minute)

When someone shares your repo link on LinkedIn/Twitter/Slack, GitHub shows a preview card.

1. **Settings** → **General** → scroll to **Social preview**
2. **Upload an image** — use local file:

```
assets/smart_water_pipeline.png
```

Recommended size: **1280 × 640 px** (GitHub crops if different; pipeline image works well).

---

## Step 5 — Wiki (optional, 15 minutes)

1. **Settings → General → Features → Wikis → ON**
2. **Wiki** tab → create pages from `docs/wiki/` (see table in previous versions of this guide)

---

## Step 6 — Verify landing page

README order after latest updates:

1. Hero image
2. Title + badges (including **CI Tests** badge)
3. Platform gallery
4. Results snapshot
5. Key metrics
6. Key deliverables
7. **Quick start** (moved up for visitors who want to run the app)
8. Learning journey (lab reports)
9. Repository structure
10. Further documentation

---

## Checklist

- [ ] About description + topics set (**manual**)
- [ ] `git push` complete
- [ ] GitHub Actions **Tests** workflow green
- [ ] Release v1.0 with 5 PDFs (**manual**)
- [ ] Social preview uploaded (**manual**)
- [ ] Wiki (optional)
