# Exercise 1 — Code smells in `legacy_hydrology.py`

**File:** `legacy_hydrology.py` (117 lines)  
**Reviewer:** Mahmudul Hasan  
**Date:** Week 4 Session A — analysis only (no refactoring yet)

---

## Summary

The script is a monolithic watershed runoff reporter: read CSV events, map land use to curve number, optionally “fetch” rainfall over HTTP (callback style), compute SCS-CN runoff, aggregate totals, and print a fixed-width table. At least **seven** distinct code smells appear; five are required for the lab and all seven are documented below with line references.

---

## Code smell checklist (≥5 required)

| # | Smell (lab category) | Where (lines / symbol) | What the code does | Why it matters |
|---|----------------------|-------------------------|--------------------|----------------|
| 1 | **Long function** | `process()` **39–104** (~66 lines) | One function opens the CSV, loads all rows into memory, loops events, performs CN lookup, sleeps, HTTP fetch via callbacks, duplicates runoff math, mutates global `STATE`, and prints the report. | Violates single responsibility; cannot unit-test runoff math without running HTTP and file I/O; any change risks breaking unrelated behavior. |
| 2 | **Magic numbers** | `calc()` **15–16**; `process()` **85–86**; implicit CN defaults **58, 60–68** | SCS-CN uses raw literals `25400`, `254`, and `0.2` with no named constants or comments tying them to USDA retention equations. Default `cn = 80` before the `if/elif` chain is unexplained. | Readers cannot verify units or formula; if the standard retention form changes, multiple literals must be hunted by hand; wrong constant edits are easy to miss. |
| 3 | **Duplicated logic** | `calc(x, y)` **13–19** vs inline block **84–92** | The same SCS-CN sequence (compute \(S\), \(I_a\), then \(Q\) with cap at \(P\)) appears twice. `calc()` exists but is **never called** from `process()`. | Formula drift: one copy could be “fixed” while the other stays wrong; doubles maintenance and hides the dead `calc()` helper. |
| 4 | **Poor naming** | `calc(x, y)` **13**; `data2` **46–48**; `p`, `lu`, `q` **55–56, 88–92**; `pth` **110** | Domain quantities are abbreviated (`x`/`y` instead of rainfall/CN; `data2` for event rows; `lu` for land use). Header row read into `hdr` **45** but never used. | Reduces readability for hydrologists and graders; obscures intent in reviews and AI refactors; unused variables suggest incomplete edits. |
| 5 | **Global mutable state** | `STATE` **9–10**; `global STATE` **41**; writes **42, 94–95** | Module-level dict holds `total_q` and `rows`; `process()` resets and fills it; report printing reads `STATE` instead of return values. | Hidden side effects: calling `process()` twice without care shares module state; tests cannot run in parallel; reasoning about data flow requires reading the whole module. |
| 6 | **Weak / missing error handling** | `fetch_rainfall` **29–30, 35–36**; `on_err` **78–79**; `__main__` **113–116**; file open **43** (no `with`) | Broad `except Exception` in network path; callback error handler **appends CSV rainfall `p`** as if it were API data (silent fallback). Top-level **bare `except:`** prints only `"failed"`. CSV file opened without context manager—no explicit handling if path missing. | Failures look like success; debugging production issues is hard; bare except hides `KeyboardInterrupt` and bug types; resource leaks possible on exceptions while file is open. |
| 7 | **Blocking I/O in hot path** | `time.sleep(0.01)` **71**; `urllib.request.urlopen` **33** inside loop **51–81** | For **each** event row, the loop sleeps 10 ms and performs a synchronous HTTP request (plus callback bookkeeping). | Runtime scales linearly with row count and network latency (~5 rows ≈ 6 s observed); cannot overlap I/O; async or batch fetch would be appropriate for real APIs. |

---

## Additional observations (supporting detail)

### Callback pattern instead of async/await
- **Where:** `fetch_rainfall(url, cb_ok, cb_err)` **22–36**; nested `on_ok` / `on_err` **75–79**.
- **Why:** Callback pyramids are harder to read than `async/await`; error propagation is split across three functions; testing requires mocking callbacks.

### Dead / unused code
- **`calc()`** is never invoked from `process()` **39–104**.
- **`hdr = next(r)`** **45** — header row discarded for logic (only `data2` body rows used).

### Presentation logic coupled to business logic
- **Where:** print loop **97–104** inside `process()`.
- **Why:** Cannot reuse runoff computation for JSON/API output without copying prints.

### Land-use → CN table duplicated by hand
- **Where:** **57–68** (if/elif chain) instead of a CSV or dict shared with Week 3 `cn_lookup.csv`.
- **Why:** Same smell as duplication—data-driven lookup would be one source of truth.

---

## Excerpts for the report

**Magic numbers and duplicate formula (`process`):**

```python
        s2 = 25400 / cn - 254
        ia2 = 0.2 * s2
        ...
        q = (p_use - ia2) ** 2 / (p_use - ia2 + s2)
```

**Silent error fallback:**

```python
        def on_err(msg):
            results.append(p)  # uses CSV P when HTTP fails
```

**Bare except in main:**

```python
    try:
        process(pth)
    except:
        print("failed")
```

---

## Exercise 1 conclusion

Documented **7** smells with line-level evidence. Refactoring (Exercise 2) should address structure, naming, constants, single SCS-CN implementation, explicit errors, removal of global `STATE`, and async or batched I/O—while preserving printed output for `data/events.csv` (Exercise 3).
