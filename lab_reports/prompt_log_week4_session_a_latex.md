# Prompt Log - Week 4 Session A

**Student:** Mahmudul Hasan (4125999049)
**Legacy:** legacy_hydrology.py (unchanged)
**Modern:** hydrology_modern.py

## Code smells found (7)

1. Long function process() lines 39-104
2. Magic numbers 25400, 254, 0.2
3. Duplicated SCS-CN calc() unused vs inline
4. Poor naming calc(x,y), data2
5. Global STATE dict
6. Weak errors bare except, silent on_err fallback
7. Blocking sleep + urlopen per row

## Refactoring summary

OpenCode prompt_refactor.txt + legacy_hydrology.py.
Split process into read_events, scs_runoff, batch_runoff, print_report, async fetch.
Callbacks to asyncio.gather + run_in_executor.
LAND_USE_CN dict; NumPy batch_runoff; Python 3.8 type hints.

## Verification

legacy_out.txt vs modern_out.txt via compare_outputs.py
MATCH: outputs identical line-by-line
TOTAL Q = 117.69226901292332

## Lessons learned

Smell documentation before AI refactor; terminal diff required despite agent claims.
