# Jagged Frontier Reflection — Smart Water Capstone

**Student:** Mahmudul Hasan (4125999049)

The **Jagged Frontier** means AI is strong on some tasks and weak on others — not uniformly "smart" or "dumb."

---

## Where AI excelled (high frontier)

| Task | Example in this project |
|------|-------------------------|
| Scaffolding | Week 7A: `SCOPE.md`, folder tree, `AGENTS.md`, README in one session |
| Repetitive code | Streamlit tab layout, pytest templates, CSV loader |
| Known patterns | SciPy `minimize_scalar` reservoir loop from lab guide |
| Documentation | Architecture diagrams, prompt log structure |

---

## Where AI struggled (low frontier)

| Task | Example | How we caught it |
|------|---------|------------------|
| Physical edge cases | Assumed P=5 mm always gives zero runoff for CN=95 | **pytest failed**; Ia is smaller for high CN |
| Unit consistency | MCM storage vs m3/s flows (Week 6) | Manual review + lab guide; `feasible_release_bounds` fix |
| Test coverage gaps | 27% with only 2 tests | Coverage report showed 0% on weather/reservoir |
| Git workflow | Wrong username at `git push` prompt | Human read terminal errors |

---

## Swiss Cheese defense (how we compensated)

1. **Human review** — units and hydrology rules before trusting merges  
2. **Unit tests** — 29 tests, 96% coverage on `src/`  
3. **Physical validation** — `src/validation.py` (Q<=P, storage bounds, monotonic flood)  
4. **Integration tests** — rainfall -> alert, full reservoir wrapper  

---

## Tool comparison (short)

| Tool | Best for this capstone |
|------|------------------------|
| **Cursor Agent** | Implementation, tests, reports in-repo |
| **ChatGPT / Gemini** | Optional second opinion on architecture (Week 7A) |
| **OpenCode** | Not required; useful in Week 1–2 for AGENTS.md pattern |

---

## What I would do differently

- Add `pytest.ini` and validation layer **before** calling the app "done."  
- Document unit conventions in the **first** prompt, not after bugs.  
- Rehearse demo script once with a timer before defense.

---

## Conclusion

AI accelerated the capstone but did not replace domain checks. The jagged frontier showed up in **small hydrology assumptions**, not in writing another Streamlit button. Tests and validation were the safety net.
