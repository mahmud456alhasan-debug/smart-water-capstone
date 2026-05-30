# Experiment 2 — SCS-CN Runoff

## Purpose

Rainfall-to-runoff transformation using USDA SCS-CN method.

## Capabilities

- `calculate_runoff(P, CN)` with Q ≤ P enforcement
- Hand reference: P=50 mm, CN=80 → **Q=13.80 mm**
- CN sensitivity curves and uncertainty band CN ∈ [75, 85]
- `validate_reference.py` CLI

## Report

[Experiment2_SCSCN_Runoff.pdf](../../release/Experiment2_SCSCN_Runoff.pdf)

## Validation

- 23 pytest cases including parametrized Q ≤ P grid
- Physical validation matrix in LaTeX report

## Role in pipeline

Provides runoff depths as plausible inflow inputs for Experiment 3 reservoir dispatch.
