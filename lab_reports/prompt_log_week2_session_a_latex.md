# Prompt Log - Week 2 Session A

## Exercise 1: Rainfall monitoring design (CoT)

**Date:** 2026-05-16

**Prompt used:**

I need to design a rainfall monitoring system. Please help me think through this step by step:

1. What data do we need to collect?
2. What API can provide real-time rainfall data?
3. How should we structure the data storage?
4. What alert thresholds make sense for flood warning?
5. How should we visualize the data?

For each step, explain your reasoning and provide code suggestions where appropriate.

**AI output summary:**

| Step | Main points from OpenCode |
|------|---------------------------|
| 1 - Data | Core: precipitation (mm), UTC timestamps, station ID, sampling interval. Derived: intensity (mm/h), rolling accumulations (1h-24h), wet/dry periods. Context: temperature, humidity, wind, pressure; IoT battery/signal. Keep raw high-resolution data; compute aggregates in storage. |
| 2 - API | Recommended **Open-Meteo** (no API key for prototyping, ~1 km grid, hourly updates, forecast). Mentioned helper `rainfall_fetcher.py`. (Week 1 Session A used OpenWeatherMap - both are valid; Open-Meteo lowers friction for labs.) |
| 3 - Storage | **TimescaleDB** hypertable on PostgreSQL (`time`, `station_id` PK), separate stations metadata and accumulated-rainfall tables; SQLite noted for smaller deployments. |
| 4 - Thresholds | Tiered table (Advisory / Watch / Warning / Emergency) using intensity and 1h, 3h, 24h accumulations aligned with WMO/NWS-style flash-flood guidance; OR logic across criteria. |
| 5 - Visualization | **Plotly** dashboard: intensity line, interval bars, 24h accumulation vs. thresholds; production options FastAPI HTML or **Grafana** on TimescaleDB. Architecture sketch: API -> fetcher -> DB -> dashboard + alert engine. |

**CoT vs shorter prompt:**

**Short prompt used:** `Design a rainfall monitoring system for urban flood warning.`

| | CoT (5-step prompt) | Short prompt |
|---|---------------------|--------------|
| Response shape | Structured design per question; tables and one pipeline diagram | Full **implementation stack** in `week2_session_a/` (Docker, FastAPI, TimescaleDB, Redis, zone-based flood model, alert router, many `.py` files) |
| Depth | Strong on *why* (data types, threshold rationale) | Strong on *how to build* (files, endpoints, urban zones) |
| Risk | Still need to verify thresholds and API terms | Easy to assume code runs without testing `docker compose` |
| Best for | Lab documentation, grading, design review | Rapid prototype when you will read and test generated code |

**Lessons learned:** Numbered CoT steps kept the answer aligned with the rubric. The short prompt produced useful code but skipped explicit step-by-step reasoning; for coursework I would start with CoT, then ask for code only after the design is approved.

---

## Exercise 2: Debugging with CoT

**Note on buggy script:** The lab guide says "receive buggy code from instructor," but the professor told the class to **do this part yourself** (no shared file). Handouts only give CoT debugging prompts, not a script. This submission uses `buggy_rainfall.py` in this folder: a short SCS-CN script with intentional errors for CoT practice.

**Bug list (your guess):**

1. **S formula wrong:** uses `25400 * CN - 254` instead of `25400 / CN - 254`.
2. **Ia wrong:** uses `0.2 * P` instead of `0.2 * S`.
3. **Missing boundary:** no `return 0` when `P < Ia`.
4. **Runoff formula wrong:** denominator uses `(P + S)` instead of `(P - Ia + S)`.
5. **No check** that `Q <= P`.

**Prompt used for AI debug:**

This code has bugs. Walk through it line by line, explain what each part should do, identify what's wrong, and suggest fixes.

(Attach or reference `buggy_rainfall.py` in OpenCode.)

**Terminal evidence (before fix):**

```text
$ python3 buggy_rainfall.py
Rainfall P = 80 mm, CN = 85
Computed runoff Q = 0.0018973275289439723 mm
```

The result is far too small (expected ~43.6 mm), which confirms the script is wrong. Main cause: `S = 25400 * CN - 254` makes S enormous (~2.16x10^6 mm), so the denominator `(P + S)` dominates and Q ~= 0.

**AI findings vs yours:**

OpenCode identified the same four core bugs I listed before running the AI prompt:

| Bug | My guess | AI finding | Match |
|-----|----------|------------|-------|
| S uses `*` not `/` | Yes | Line 9: `25400 * CN` inflates S to ~2.16x10^6 mm | Yes |
| Ia uses `0.2 * P` not `0.2 * S` | Yes | Line 12: wrong base for initial abstraction | Yes |
| No `P <= Ia` return | Yes | Line 14: missing early return; spurious Q when P < Ia | Yes |
| Denominator `(P + S)` | Yes | Line 17: should be `(P - Ia + S)` | Yes |

The AI's corrected function matches `rainfall_fixed.py` (Q ~= 43.3-43.6 mm for P=80, CN=85). **Note:** At the end of the chat, the AI claimed the fully buggy script might give ~48.9 mm on this input; my **terminal run** of `buggy_rainfall.py` gave **~0.002 mm** because the huge erroneous S dominates the denominator-so I trusted the local run over that closing sentence and verified the fix with `rainfall_fixed.py` -> **43.6 mm**.

**Final fix summary:**

Changes in `rainfall_fixed.py`:

1. `S = (25400 / CN) - 254`
2. `Ia = 0.2 * S`
3. `return 0.0` when `P < Ia`
4. `Q = (P - Ia)**2 / (P - Ia + S)`
5. `return min(Q, P)` so runoff cannot exceed rainfall

**Terminal evidence (after fix):**

```text
$ python3 rainfall_fixed.py
Rainfall P = 80 mm, CN = 85
Computed runoff Q = 43.6 mm
```

Matches Week 1 Session B hand calculation (P=80, CN=85 -> Q~=43.6 mm). **Tests pass** for this case.

---

## Personal prompting strategy guide (draft)

**Use CoT when:**

- Multi-step hydrology (unit conversions, SCS-CN, reservoir balances).
- System design (data -> API -> storage -> alerts -> visualization).
- Debugging when the failure mode is unclear; ask for line-by-line reasoning.
- Any work you must **show and verify** for a grade.

**Use shorter prompts when:**

- You already have an approved design and only need code (e.g. "implement the fetcher from step 2").
- Small edits (fix a variable name, add one test case).

**Always verify:**

- Formulas and units (mm vs mm/h; SCS-CN: S, Ia, Q <= P).
- API keys in environment variables, not in repo or AGENTS.md.
- Thresholds against local standards and course lab values (e.g. 20 mm/h alert in Week 5 Lab 1).
- Run `python3` locally after AI fixes; compare to hand calculation or Week 1 Session B numbers.
