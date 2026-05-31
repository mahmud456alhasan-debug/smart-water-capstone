# Prompt Log - Week 4 Session A

**Student:** Mahmudul Hasan (4125999049)  
**Lab:** Refactoring & Migration Practice  
**Legacy file:** `legacy_hydrology.py` (unchanged)  
**Modern file:** `hydrology_modern.py`

---

## Code smells found (≥5)

Analysis completed in Exercise 1. Full worksheet: `code_smells_worksheet.md`.

1. **Long function** — `process()` lines 39–104 (CSV, CN, HTTP, calc, print).
2. **Magic numbers** — `25400`, `254`, `0.2` without named constants.
3. **Duplicated logic** — `calc()` never called; formula duplicated at 84–92.
4. **Poor naming** — `calc(x,y)`, `data2`, unused `hdr`.
5. **Global mutable state** — module-level `STATE` dict.
6. **Weak errors** — bare `except:`, silent `on_err` fallback to CSV rainfall.
7. **Blocking I/O in loop** — `time.sleep(0.01)` + sync `urlopen` per row.

---

## Refactoring summary

**Prompt used:** `prompt_refactor.txt` + full pasted `legacy_hydrology.py` (OpenCode Desktop, folder `week4_session_a/`).

**Largest structural change:** Monolithic `process()` split into `read_events`, `cn_for_land_use`, `scs_runoff`, `batch_runoff`, `print_report`, and async path `_process_async` / `fetch_rainfall_async`. Global `STATE` removed; results are local.

**Async changes (what is now awaitable):**
- Legacy callback `fetch_rainfall(url, cb_ok, cb_err)` replaced with `fetch_rainfall_async` using `asyncio` + `run_in_executor` (thread pool for blocking `urlopen`).
- Per-row HTTP gathered concurrently (`asyncio.gather`) instead of sequential blocking calls in the loop.
- Entry: `asyncio.run(_process_async(path))` from `main()`.

**AI change summary (smells addressed):**

| Smell | Fix |
|--------|-----|
| Global `STATE` | Local variables and return values |
| Callback HTTP | `async`/`await` + executor |
| God function | Multiple named functions |
| Duplicate CN if/elif | `LAND_USE_CN` dict + `DEFAULT_CN` |
| Dead `calc()` | Single `scs_runoff()` |
| Bare / broad except | Specific exception types |
| Silent fallback | `Optional[float]`; explicit `None` → use CSV P |
| `time.sleep` per row | Removed |
| List-of-lists CSV | `csv.DictReader` |
| Magic numbers | Constants + `compute_s` / `initial_abstraction` |
| Type hints | `Union`/`Optional` (Python 3.8) |
| Batch math | NumPy `batch_runoff()` after I/O |

**Files:** `hydrology_modern.py` created; `legacy_hydrology.py` left untouched (verified).

---

## Verification

**Commands run:**

```bash
cd week4_session_a
python3 legacy_hydrology.py data/events.csv > legacy_out.txt
python3 hydrology_modern.py data/events.csv > modern_out.txt
python3 compare_outputs.py legacy_out.txt modern_out.txt
```

**Tests / comparisons run:** Line-by-line diff of stdout via `compare_outputs.py`.

**Behavior match:** **Yes** — `MATCH: outputs identical line-by-line`.

**Sample output (both scripts):**

- Row Q values: 5.8128, 13.8025, 19.6124, 53.8981, 24.5665 mm  
- `TOTAL Q = 117.69226901292332`  
- Report header unchanged: `=== LEGACY RUNOFF REPORT ===`

**Performance (rough):** Legacy ~6 s for 5 rows (0.01 s sleep × 5 + sequential HTTP). Modern run ~7 s in one verification (concurrent HTTP, no sleep)—similar on small N; modern should scale better for many rows because I/O is gathered, not sequential.

**Domain check:** Q values match Week 3 Session A `batch` for the same `data/events.csv` land uses and rainfall.

---

## Lessons learned

Documenting smells with line numbers before prompting produced a focused refactor list. OpenCode matched byte-for-byte output when asked explicitly—terminal `compare_outputs.py` still required to verify. Async helped the callback pattern but exact output parity mattered more than performance on five rows. Keeping the legacy file unchanged made Exercise 3 comparison straightforward.
