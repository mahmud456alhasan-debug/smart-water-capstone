# Experiment 4 — Flood Inundation

## Purpose

Impact assessment stage — spatial flood consequences on synthetic DEM.

## Capabilities

- 100×100 synthetic DEM (seed 42)
- Bathtub inundation: depth, area %, volume vs water level
- Stage curve 40–50 m (0.5 m steps), monotonicity checks
- Seed sensitivity (seeds 42, 7, 99)
- `validate_flood.py` — **9/9 PASS**

## Report

[Experiment4_Flood_Inundation.pdf](../../release/Experiment4_Flood_Inundation.pdf)

## Limitations

Bathtub model — no BFS routing or hydrodynamics (documented in threats to validity).

## Role in pipeline

Translates hydrologic and operational inputs into inundation maps for planning and communication.
