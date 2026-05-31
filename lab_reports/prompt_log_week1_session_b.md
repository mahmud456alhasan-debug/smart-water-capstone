# Prompt Log - Week 1 Session B

## Exercise 1: Reservoir storage (CoT)

**Date:** 2026-05-16

**Prompt used:**

I need to calculate the water storage capacity of a reservoir.
The reservoir has a surface area of 500 hectares and an average depth of 15 meters.

Please solve this step by step:
1. Convert hectares to square meters
2. Calculate volume in cubic meters
3. Convert to million cubic meters (MCM)
4. Verify the calculation makes sense for a medium-sized reservoir

Show your reasoning at each step.

**AI output summary:**

OpenCode returned a four-step chain-of-thought solution: (1) 500 ha = 5,000,000 m² using 1 ha = 10,000 m²; (2) volume = 5,000,000 m² × 15 m = 75,000,000 m³; (3) 75 MCM; (4) sanity check that 75 MCM lies in a typical medium-reservoir range (about 10–100 MCM), with brief comparison to smaller and very large impoundments.

**Verification:**

- Unit chain: hectares → m² → m³ → MCM is consistent (MCM = m³ / 10⁶).
- Arithmetic: 500 × 10,000 = 5,000,000; × 15 = 75,000,000 m³; ÷ 10⁶ = 75 MCM.
- Magnitude: 75 MCM is plausible for a medium-sized storage project; the AI’s qualitative check is reasonable for coursework (not a substitute for site-specific design data).

**Lessons learned:**

Numbered steps in the prompt produced a response that was easy to audit step-by-step. Explicit “verify reasonableness” encouraged a short engineering judgment, not only algebra.

---

## Exercise 2: Direct vs CoT (SCS-CN)

**Direct prompt:**

Calculate the runoff for 80mm rainfall with CN=85

**Direct response summary:**

Despite the short prompt, the model still showed intermediate steps: S = 44.82 mm, Ia = 8.96 mm, check P > Ia, then Q = 43.6 mm using the SCS-CN formula, plus a runoff-ratio comment (~54.5%).

**CoT prompt:**

Calculate the runoff for 80mm rainfall with CN=85. Show each step: (1) Calculate S, (2) Calculate Ia, (3) Apply SCS-CN formula, (4) Verify Q ≤ P

**CoT response summary:**

Same intermediate values (S = 44.82 mm, Ia = 8.96 mm) and final Q = 43.6 mm. Step 4 explicitly verified Q ≤ P (43.6 mm ≤ 80 mm) and interpreted the remainder as infiltration plus initial abstraction.

**Comparison:**

- **Numeric result:** Both prompts gave **Q = 43.6 mm** (consistent with manual check).
- **Transparency:** Direct prompt still showed work in this case; CoT prompt **required** the audit step Q ≤ P, which is valuable for grading and for catching impossible results.
- **When to use each:** Use a **direct** prompt for quick checks when you already know the method. Use **CoT** for coursework, design documentation, and any problem where you must show verification steps to an instructor or reviewer.
