# AI Failures We Found

**Mahmudul Hasan (4125999049)** · Smart Water Lab

Concise table for Assignment 3 & 4 graders: **AI output → why wrong → how detected → fix**.

Full chains: [assignment3/EVIDENCE_CHAIN.md](../assignment3/EVIDENCE_CHAIN.md) · Attribution: [assignment3/CODE_ATTRIBUTION.md](../assignment3/CODE_ATTRIBUTION.md)

---

## Master table (capstone + experiments)

| AI output | Why wrong | How detected | Fix |
|-----------|-----------|--------------|-----|
| `S = 25400 * CN - 254` | Uses × not ÷; S enormous | Terminal Q≈0.002 vs ~43.6 mm; hand calc | `S = 25400/CN - 254` in `scs_runoff_mm` / Exp2 |
| `Ia = 0.2 * P` | Ia must use S, not P | Same Week 2 debug session | `Ia = 0.2 * S` |
| “P=5 mm, CN=95 → Q always 0” | Ia≈2.67 mm; P=5 gives Q≈0.34 | `demo_wrong_assumption_fails.py`; regression test | Correct test inputs; document in prompt_log |
| Runoff formula without Q≤P cap | Violates water balance | Parametrized pytest grid | `min(Q, P)` + `validate_runoff_mm` |
| Missing `rain` in API JSON | Crashes dry cities | 50-city pytest mocks | Return 0 mm/h |
| Hardcoded API key | Security | Code review | Env var only |
| SLSQP infeasible start | Storage violates bounds | `validate_schedule()` | trust-constr + feasible x₀ |
| Fake feasible eco trade-off points | Misleading plot | Hydrology review | Mark infeasible honestly |
| Flood depth without floor | Negative depth | Physical checklist | `max(0, ·)` |
| Wet mask with `≤` elev | Edge cell wrong | validate_flood CLI | Strict `<` mask |

---

## Capstone-only (Assignment 3 headline cases)

| AI output | Why wrong | How detected | Fix |
|-----------|-----------|--------------|-----|
| Test assumes Q(5,95)=0 | Contradicts SCS-CN Ia | AssertionError in demo script | `test_hallucination_cn95_p6_produces_runoff` |
| Low pytest coverage (27%) | weather/reservoir untested | `pytest --cov` | Expanded to 33 tests, 96% on `src/` |

---

## Swiss Cheese — which layer caught what

| Error type | Layer that caught it |
|------------|---------------------|
| Wrong formula | Hand calc + validation CLI |
| API edge case | pytest mocks |
| False “always zero” assumption | Boundary test + formula review |
| Optimizer infeasibility | `validate_schedule()` |
| Unit mix-ups (MCM vs m³/s) | Manual code review |

---

## Statistics

| Metric | Value |
|--------|------:|
| AI outputs reviewed | 52 |
| Corrections documented | **9** |
| Capstone pytest | **33** |
| Full experiment pytest | **88** |

---

## Physical validity link

Each fix above maps to a rule in [docs/PHYSICAL_VALIDATION.md](../docs/PHYSICAL_VALIDATION.md).
