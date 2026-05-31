# Assignment 3 — Swiss Cheese Test Suite

**Mahmudul Hasan (4125999049)** · Xi'an Jiaotong University · 2026  
**Course:** AI-Augmented Software Engineering · **Weight:** 20% · **Due:** Week 12

---

## Start here (for graders)

| Priority | File | Purpose |
|----------|------|---------|
| **1** | [README.md](README.md) | This page |
| **2** | [SWISS_CHEESE_REPORT.pdf](SWISS_CHEESE_REPORT.pdf) | Swiss Cheese narrative (LMS) |
| **3** | [HALLUCINATION_CASE_STUDY.pdf](HALLUCINATION_CASE_STUDY.pdf) | Primary hallucination case (LMS) |
| **4** | [tests/](../tests/) + [evidence/](evidence/) | **33 pytest** + buggy/fixed code |

Markdown sources: [SWISS_CHEESE_REPORT.md](SWISS_CHEESE_REPORT.md) · [HALLUCINATION_CASE_STUDY.md](HALLUCINATION_CASE_STUDY.md)

**Optional (supporting detail):** [EVIDENCE_CHAIN.md](EVIDENCE_CHAIN.md) · [CODE_ATTRIBUTION.md](CODE_ATTRIBUTION.md) · [docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md) · [docs/GRADER_AUDIT.md](../docs/GRADER_AUDIT.md)

---

## What this assignment proves

Layered verification caught **AI-assisted mistakes** before trusting hydrology code — not “tests pass” alone.

**Strongest story (Case B):**

```text
AI-assisted / draft SCS-CN code  →  wrong formula  →  terminal + tests  →  fix  →  regression tests
```

Evidence: [`evidence/buggy_rainfall.py`](evidence/buggy_rainfall.py) → [`evidence/rainfall_fixed.py`](evidence/rainfall_fixed.py) → [`src/runoff/scs_cn.py`](../src/runoff/scs_cn.py)

Reproduce failure: `python3 assignment3/scripts/demo_wrong_assumption_fails.py`

---

## Tests (capstone repo only)

**33 automated pytest cases** in [`tests/`](../tests/) — this is what GitHub Actions runs.

```bash
pytest -q   # expect 33 passed
```

Additional **88 experiment tests** live in local `ai_water_lab/experiment*` folders (not in this repo). See [docs/TEST_COUNTS.md](../docs/TEST_COUNTS.md).

---

## Swiss Cheese layers

```text
AI draft / review  →  pytest (33)  →  validation.py  →  integration tests  →  trusted result
```

---

## Related assignments

| # | Folder |
|---|--------|
| 1 | [assignment1/](../assignment1/) |
| 2 | [assignment2/](../assignment2/) |
| 3 | **this folder** |
| 4 | [assignment4/](../assignment4/) |

---

## Regenerate PDFs

```bash
cd assignment3
pdflatex SWISS_CHEESE_REPORT.tex && pdflatex SWISS_CHEESE_REPORT.tex
pdflatex HALLUCINATION_CASE_STUDY.tex && pdflatex HALLUCINATION_CASE_STUDY.tex
rm -f *.aux *.log *.out
```
