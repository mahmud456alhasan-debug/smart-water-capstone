# Week 8 Session A - Testing and Validation

Tool: Cursor Agent | Date: 2026-05-22

## Exercise 1: Comprehensive tests

Prompt (from lab guide): Write pytest tests with normal, edge, invalid, and physical cases; fixtures; target >80% coverage for capstone src/ functions.

Added: tests/test_runoff.py, test_weather.py, test_flood.py, test_reservoir.py, test_validation.py, test_integration.py, tests/conftest.py.

Hallucination found: Assumed P=5 mm always below Ia for CN=95; high CN lowers Ia so runoff was non-zero. Fixed test to use P=2 mm, CN=80.

Result: 29 passed; coverage 96% on src/ (pytest -q --cov=src --cov-report=term-missing).

## Exercise 2: Swiss Cheese Model

Layer 1 - Code review: Manual review of units in reservoir/flood modules.
Layer 2 - Unit tests: 29 pytest cases.
Layer 3 - Physical validation: src/validation.py (Q<=P, storage bounds, monotonic flood).
Layer 4 - Integration: tests/test_integration.py workflows.

## Screenshot

week8_session_a_terminal.png - pytest + coverage table (96%).

## Lessons learned (Session 8)

Swiss Cheese layers map cleanly to validation.py plus integration tests. Coverage exposes untested reservoir and weather modules quickly. Always verify SCS-CN Ia before assuming zero runoff.
