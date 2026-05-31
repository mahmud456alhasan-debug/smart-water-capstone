# Prompt Log - Week 3 Session A

## Story → spec (brief)

**User story:** As a hydrologist, I want to calculate SCS-CN runoff for different land use types so that I can estimate flood risk for my watershed.

**Technical spec (before prompting):**

- **Actor / goal:** Hydrologist; runoff by land use for flood-risk screening.
- **Inputs:** Rainfall depth P (mm); curve number CN per land use (or land-use → CN lookup table); optional watershed id.
- **Outputs:** Runoff depth Q (mm); summary tables and/or plots; assumptions documented (Ia = 0.2S, Q = 0 if P < Ia, Q <= P).
- **Quality bar:** Unit tests for edge cases (P=0, P<Ia, CN bounds, Q <= P); clear errors for invalid CN or negative rainfall.
- **Formulas:** S = 25400/CN - 254; Ia = 0.2*S; Q = (P-Ia)^2/(P-Ia+S) when P > Ia.

---

## Scaffolding generation

**Prompt used:** See `scaffold_prompt.txt` (user story + 7 deliverables + technical spec bullets; read existing `data/cn_lookup.csv` and `data/sample_rainfall.csv`).

**Where saved:** `ai_water_lab/week3_session_a/`

**What matched my spec:**

- Directory layout: `src/`, `tests/`, `data/`
- `calculate_runoff(P, CN)` with Ia, Q=0 when P < Ia, Q clipped to P
- `data_loader.py` for CSV with validation
- `visualization.py` and CLI (`single`, `batch`, `table`, `plot`)
- 18 pytest cases (edge cases, vectorised, integration)
- `requirements.txt`, `README.md`; no fake API keys

**What was wrong or generic at first:**

- Type hints used `X | Y` syntax (invalid on Python 3.8); OpenCode fixed to Union/Optional.
- Some test expected values were wrong until recalculated against the formula.
- OpenCode summary mentioned six land uses; `cn_lookup.csv` has five rows (minor wording slip).

**Changes made in Exercise 2 (customize):**

- README: author Mahmudul Hasan, student ID 4125999049, `python3` commands, venv note.
- Kept domain files `data/cn_lookup.csv`, `data/sample_rainfall.csv`.
- Generated `runoff_curves.png` via CLI plot command.
- Created `.venv`, installed requirements, re-ran batch and pytest locally.

---

## Cold-start reflection

**What would have been harder without scaffolding:** Empty-repo start would require choosing package layout, writing test stubs, CLI entry points, README, and requirements from scratch before focusing on hydrology.

**What I still had to decide myself:** CN values per land use in CSV, sample watershed events, trusting terminal over AI test numbers until pytest passed, using `python3` vs `python` on Linux, and verifying P=80 mm / CN=85 → Q ≈ 43.55 mm (consistent with Week 1 Session B and Week 2 debug lab).

---

## Lessons learned

Story → spec before the scaffold prompt improved alignment. Four OpenCode screenshots document one long session (not four separate prompts). Always run `pytest` and a known SCS-CN case locally after AI generation.
