# Prompt Log - Week 3 Session A

## Story -> spec (brief)

**User story:** As a hydrologist, I want to calculate SCS-CN runoff for different land use types so that I can estimate flood risk for my watershed.

**Technical spec (before prompting):**

- Actor / goal: Hydrologist; runoff by land use for flood-risk screening.
- Inputs: Rainfall depth P (mm); CN per land use or lookup table; optional watershed id.
- Outputs: Runoff Q (mm); tables/plots; assumptions (Ia = 0.2S, Q = 0 if P < Ia, Q <= P).
- Quality bar: edge-case tests; clear errors for bad CN or negative P.
- Formulas: S = 25400/CN - 254; Ia = 0.2*S; Q = (P-Ia)^2/(P-Ia+S) when P > Ia.

---

## Scaffolding generation

**Prompt used:** See scaffold_prompt.txt in week3_session_a/.

**Where saved:** ai_water_lab/week3_session_a/

**What matched my spec:**

- src/, tests/, data/ layout
- calculate_runoff(P, CN) with correct boundary conditions
- data_loader.py, visualization.py, cli.py (single, batch, table, plot)
- 18 pytest tests; requirements.txt; README.md
- No fake API keys

**What was wrong or generic at first:**

- Python 3.8 incompatible type hints (X | Y); fixed by agent
- Wrong test expected values until recalculated
- Minor summary typo (land-use count)

**Exercise 2 customize:**

- README author and student ID; python3 commands
- runoff_curves.png from plot CLI
- .venv created after apt install python3.8-venv

---

## Cold-start reflection

Without scaffolding: slow cold start on folders, tests, README.
Still human: CSV domain data, verify P=80 CN=85 -> 43.55 mm, run pytest locally.

## Lessons learned

Spec-first prompting; one long OpenCode session (4 screenshots); terminal verification required.
