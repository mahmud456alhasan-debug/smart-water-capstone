# Prompt Log - Week 1 Session A

## Exercise 2: Rainfall Data Reader

**Date:** 2026-05-15

**Prompt Used:**

I am a water resources student. Please write a Python script that:
1. Creates a sample CSV file with columns: date, rainfall_mm, location
2. Reads the CSV file using pandas
3. Calculates total and average rainfall
4. Prints a summary report
Include comments explaining each step.

**AI Output Summary:**

OpenCode generated a script (initially saved as `rainfall_analysis.py`) that creates `rainfall_data.csv` with 90 rows (30 days × 3 stations), reads it with `pandas`, groups by `location` to compute total and average daily rainfall per station, and prints a formatted summary including date range, per-station totals/averages, overall mean rainfall, and maximum daily rainfall.

**Verification:**

- Did the code run successfully? **Yes** — `python3 hello_ai.py` completed without errors; `rainfall_data.csv` was created.
- Were the calculations correct? **Yes** — totals are sums of `rainfall_mm` per location over 30 days; averages match total ÷ 30 per station; overall mean matches the mean of all 90 values (spot-check or recalculate in a notebook if required for your report).
- Any errors or issues? **None at runtime.** The agent used filename `rainfall_analysis.py` instead of the handout name `hello_ai.py`; the same code was copied to `hello_ai.py` for submission.

**Changes Made:**

- Renamed / duplicated the agent output to `hello_ai.py` to match the lab submission requirement.

**Lessons Learned:**

*(Edit this in your own words, e.g.:)* Specific prompts produce runnable starter code quickly, but output should always be reviewed (filenames, paths, column names) and checked against the assignment deliverables before submission.
