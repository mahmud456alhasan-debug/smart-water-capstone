# Prompt Log - Week 6 Session A Lab 3

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** Water Resources Optimization

---

## Formulation

**Decision variables:** One release rate Q (m3/s) per day (7 sequential single-variable optimizations)

**Unit convention (MCM vs m3/s):** Storage in MCM; inflow/release in m3/s; daily volume = flow x 0.0864 MCM/(m3/s)/day; balance S[t+1] = S[t] + I_vol - R_vol

**Revenue model:** revenue = price[$/MWh] x (power_MW x 24); power_MW = HEAD x ETA x 9.81e-3 x Q_release; HEAD=80 m, ETA=0.85

**Scalar objective:** Maximize revenue; eco flow enforced as lower bound on release (not weighted multi-objective)

**Prompts used:** `prompt_optimize.txt`, `prompt_tradeoff.txt`

---

## Results

**Total revenue (units):** ~708,849 USD (7-day sum, eco=10 m3/s baseline)

**Trade-off figure path:** `figures/tradeoff_revenue.png`

**Trade-off trend:** Eco 5-15 m3/s all feasible; revenue nearly flat because storage bounds (not eco minimum) limit release on late days

---

## Validation

**Worst constraint violation (if any):** None after storage-aware release bounds; min storage slack 0.000 MCM on day 7

**Checklist:** storage in [50,200] MCM; release in [10,150] m3/s; release >= eco; water balance within tolerance

---

## Lessons learned

Converting m3/s to MCM/day (factor 0.0864) before the storage balance is essential. Storage-feasible release bounds were needed on day 7. Three terminal screenshots are enough for submission; OpenCode was not required by the Week 6 lab guide. When the eco-flow trade-off curve is flat, check whether storage--not ecology--is the active constraint.
