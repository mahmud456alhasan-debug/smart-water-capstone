# Experiment 1 — Rainfall Alert

## Purpose

Monitoring and early-warning stage of the Smart Water pipeline.

## Capabilities

- OpenWeather current weather + 5-day/3-hour forecast
- GREEN / YELLOW / RED classification (<10, 10–20, ≥20 mm/h)
- 3-hour and 6-hour forecast risk pipeline
- 50-city batch CLI validation
- Streamlit dashboard with demo storm mode

## Report

[Experiment1_Rainfall_Alert.pdf](../../release/Experiment1_Rainfall_Alert.pdf)

## Validation

- 20 pytest cases (mocked API)
- Missing `rain` field → 0 mm/h
- `audit_summary.txt` in submission appendix

## Role in pipeline

Supplies rainfall observations and intensity estimates for Experiment 2 runoff modeling.
