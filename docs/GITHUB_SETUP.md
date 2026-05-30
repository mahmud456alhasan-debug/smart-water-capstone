# GitHub repository setup

Do these steps on [smart-water-capstone](https://github.com/mahmud456alhasan-debug/smart-water-capstone) after `git push`.

---

## Step 1 — About section (highest impact, 2 minutes)

On the repo home page, click the **gear icon** next to "About".

**Description** (paste exactly):

```
AI-Augmented Smart Water Lab featuring rainfall monitoring, runoff modeling, reservoir optimization, flood analysis and engineering validation.
```

**Topics** (add each):

```
hydrology
water-resources
streamlit
python
optimization
flood-modeling
reservoir-optimization
pytest
ai-engineering
decision-support
```

Save. The empty "No description" box disappears immediately.

---

## Step 2 — Push latest README

```bash
cd ~/Downloads/Software\ Development/ai_water_lab/capstone
git push origin main
```

If commit needed first:

```bash
echo "Premium README, release PDFs, wiki pages" > /tmp/msg.txt
git add README.md release/ docs/wiki/
git commit -F /tmp/msg.txt
git push origin main
```

---

## Step 3 — Create Release v1.0 (5 minutes)

**Releases → Draft a new release**

| Field | Value |
|-------|--------|
| Tag | `v1.0.0` |
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

## Step 4 — Populate Wiki (15 minutes, optional)

1. **Settings → General → Features → Wikis → ON**
2. Click **Wiki** tab → **Create the first page**
3. Copy content from `docs/wiki/Home.md`
4. Create pages (New Page) from each file in `docs/wiki/`:
   - Experiment-1-Rainfall-Alert.md
   - Experiment-2-SCSCN-Runoff.md
   - Experiment-3-Reservoir-Optimization.md
   - Experiment-4-Flood-Inundation.md
   - AI-Engineering-Portfolio.md

---

## Step 5 — Verify landing page

After push, confirm README shows in order:

1. Title + professional intro
2. Badges
3. Quick navigation links
4. **Pipeline banner image**
5. Engineering outcomes
6. Metrics + submission table
7. 2×2 screenshot gallery
8. Quick start

---

## Checklist

- [ ] About description + topics set
- [ ] `git push` complete
- [ ] Release v1.0 with 5 PDFs from `release/`
- [ ] Wiki home + 5 pages (optional)
- [ ] No `__pycache__` in file tree

## Repository rename (optional, skip if already submitted)

Current name `smart-water-capstone` is fine for coursework. Portfolio alternative: `smart-water-lab-suite` (requires GitHub Settings → rename + update local remote).
