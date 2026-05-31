# 5-Minute Presentation — Strict Timing

**Mahmudul Hasan (4125999049)** · Assignment 4 defense  
**Total:** 5:00 · Rehearse with phone timer

---

## 0:00 – 1:00 · Problem

**Say:**
- “Urban water managers need one view: rain intensity, runoff, reservoir releases, and flood extent.”
- “Our course labs built four separate Python modules; the capstone integrates them in one Streamlit app.”
- “Domain: hydrology / smart water — real constraints like **runoff cannot exceed rainfall**.”

**Show:** GitHub repo or pipeline hero image (`assets/smart_water_pipeline.png`).

---

## 1:00 – 2:00 · Architecture

**Say:**
- “Pipeline: Weather CSV → SCS-CN runoff → 7-day reservoir dispatch → DEM flood map.”
- “Code layout: `app/main.py` + four `src/` packages + `validation.py` physical checks.”
- “33 pytest tests, 96% coverage on `src/`; 88 tests across all experiments.”

**Show:** README architecture diagram or four-tab Streamlit header.

---

## 2:00 – 3:00 · Live demo

Follow [DEMO_SCRIPT.md](DEMO_SCRIPT.md) — **15 s per tab**:

| Time | Tab | One line |
|------|-----|----------|
| 2:00 | Weather | RED alert at 22 mm/h from sample CSV |
| 2:15 | Runoff | P=50, CN=80 → Q≈13.8 mm, **Q ≤ P** green |
| 2:30 | Reservoir | ~$708k revenue, validation PASS |
| 2:45 | Flood | Raise stage 50→60 m, flooded % increases |

**Backup:** `week7_session_b_Streamlit_page.png` + `pytest -q` terminal.

---

## 3:00 – 4:00 · AI failures (Jagged Frontier)

**Say:**
- “We used **Cursor Agent** for scaffold and tests — not OpenCode for the capstone.”
- **Case 1:** AI-style formula `25400*CN` → terminal showed Q≈0 instead of ~44 mm → fixed division form.”
- **Case 2:** AI assumed P=5 mm always zero runoff for CN=95 → pytest showed Q≈0.34 mm.”
- “Nine AI corrections documented; Swiss Cheese: review + pytest + `validation.py`.”

**Show:** [assignment4/AI_FAILURES.md](../assignment4/AI_FAILURES.md) or one slide table.

---

## 4:00 – 5:00 · Tool evaluation & close

**Say (tool comparison — rubric marks):**

| Tool | Strengths | Weaknesses |
|------|-----------|------------|
| **Cursor Agent** | Fast scaffold, tests, in-repo edits | Hydrology edge assumptions |
| **ChatGPT** | Rubric alignment, second opinion | No direct repo integration |
| **Gemini** | Optional architecture review | Same hallucination risks |
| **OpenCode** | Week 1–2 AGENTS.md pattern | Not used for capstone code |

**Close:**
- “Repo is public; `streamlit run app/main.py`; all PDFs in `submission/`.”
- “Physical rules in `docs/PHYSICAL_VALIDATION.md`; prompt log shows every correction.”

---

## Timing checklist

| Block | Target | Done? |
|-------|--------|-------|
| Problem | 0:00–1:00 | [ ] |
| Architecture | 1:00–2:00 | [ ] |
| Demo | 2:00–3:00 | [ ] |
| AI failures | 3:00–4:00 | [ ] |
| Tool evaluation | 4:00–5:00 | [ ] |

**Practice run time:** _____ min _____ sec (fill after rehearsal)

---

## Related

- [DEMO_SCRIPT.md](DEMO_SCRIPT.md) — tab-by-tab clicks  
- [docs/JAGGED_FRONTIER.md](JAGGED_FRONTIER.md) — full reflection  
- [assignment4/RUBRIC_MAPPING.md](../assignment4/RUBRIC_MAPPING.md) — rubric evidence
