# Hallucination Case Study — Assignment 3

**Mahmudul Hasan (4125999049)** · Primary case for Swiss Cheese Test Suite deliverable

---

## Case: False SCS-CN “zero runoff” assumption

This is the **flagship example** for Assignment 3: an AI-assisted assumption that sounded plausible but was **physically wrong** for high curve numbers.

---

## Step 1 — AI claim / assumption

During Week 8 Session A test design (Cursor Agent, guided by lab worksheet), the working assumption was:

> For **CN = 95** (very impervious watershed) and **P = 5 mm**, rainfall is always below initial abstraction **Ia**, so **runoff Q = 0**.

This mirrors a common LLM pattern: treat “high CN → less infiltration” as “any small storm produces zero runoff,” without computing Ia.

**SCS-CN initial abstraction:**

```text
Ia = 0.2 × (25400/CN − 254)   [mm]
```

For **CN = 95**:

```text
S  = 25400/95 − 254 ≈ 13.37 mm
Ia = 0.2 × S ≈ 2.67 mm
```

So **P = 5 mm > Ia** → **Q ≈ 0.34 mm** (not zero). The AI verbal rule fails on its own example pair.

For **CN = 80**: Ia ≈ 20.3 mm → P = 5 mm → Q = 0 ✓

---

## Step 2 — Test created

File: [`../tests/test_runoff.py`](../tests/test_runoff.py)

```python
def test_runoff_below_initial_abstraction():
    assert scs_runoff_mm(2.0, 80.0) == 0.0

def test_runoff_not_exceed_rainfall_high_cn():
    p = 100.0
    for cn in (60.0, 80.0, 95.0):
        q = scs_runoff_mm(p, cn)
        assert q <= p + 1e-6
```

Physical validator: [`../src/validation.py`](../src/validation.py) — `validate_runoff_mm()` enforces **Q ≤ P**.

---

## Step 3 — Failure discovered

When running **`scs_runoff_mm(5.0, 95.0)`**, the result was **Q ≈ 0.34 mm** — not zero. That directly contradicts the AI assumption.

**pytest:** `test_hallucination_cn95_p6_produces_runoff` — **33 passed** total.

Documented in [`../prompt_log.md`](../prompt_log.md):

> *Hallucination found: Assumed P=5 mm always below Ia for CN=95; high CN lowers Ia so runoff was non-zero. Fixed test to use P=2 mm, CN=80.*

---

## Step 4 — Fix applied

| Action | Detail |
|--------|--------|
| Correct zero-runoff test | Use **P = 2 mm, CN = 80** where Ia ≈ 20.3 mm |
| Add physical sweep | `test_runoff_not_exceed_rainfall_high_cn` for CN 60/80/95 |
| Add validator | `validate_runoff_mm(p, q)` — fails if Q > P |
| Document | Week 8A report + this case study |

---

## Step 5 — Lessons learned

1. LLMs conflate **infiltration behavior** with **algebraic Ia thresholds**.  
2. Boundary tests must include **CN extremes** (low and high), not only mid-range CN = 80.  
3. The Swiss Cheese layer that caught this was **human review + pytest**, not the AI’s self-check.  
4. This single narrative satisfies Assignment 3’s **“≥1 hallucination”** requirement with reproducible evidence.

---

## Secondary cases (experiments)

Nine additional AI corrections across Experiments 1–4 are tabulated in [`../assignment4/AI_FAILURES.md`](../assignment4/AI_FAILURES.md), including:

- Wrong SCS formula variant (Exp 2)  
- Missing `rain` field crash (Exp 1)  
- Infeasible reservoir optimizer seed (Exp 3)  
- Flood depth without `max(0, ·)` (Exp 4)  

---

## Evidence checklist (for grader)

- [x] AI prompt documented — `prompt_log.md` Week 8A  
- [x] Tests in repo — `tests/test_runoff.py`, `tests/test_validation.py`  
- [x] Failure / assumption documented — this file + Week 8A lab report PDF  
- [x] Fix applied — corrected tests + `validation.py`  
- [x] Runnable — `pytest -q` → **33 passed**
