#!/usr/bin/env python3
"""
Specialized Experiment 3: 7-day reservoir dispatch optimization.

Unit convention (documented in formulation.md and prompt_log.md):
  - Storage V in m^3
  - Inflow and release Q in m^3/s (daily average)
  - Timestep DT = 86400 s (one day)
  - Daily volume from flow: Vol = Q * DT  (m^3)

Revenue model:
  - Turbine head H = 80 m, efficiency eta = 0.85
  - Power (kW) = eta * rho * g * H * Q / 1000,  Q in m^3/s
  - Energy (kWh/day) = Power_kW * 24
  - Revenue ($/day) = price ($/kWh) * Energy_kWh

Multi-objective handling:
  - Hard constraint: Q_release >= Q_eco via optimizer bounds
  - Maximize hydropower revenue (ecological deficit = 0 when bounds enforced)

Solver: scipy.optimize.minimize (trust-constr primary; SLSQP cross-check).
Sequential optimize_day() provided for pedagogy and cross-check.
"""

from __future__ import annotations

import csv
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize, minimize_scalar

# --- Experiment 3 parameters (guide) ---
V0 = 500_000.0
V_MIN, V_MAX = 100_000.0, 1_000_000.0
Q_ECO, Q_MAX = 10.0, 100.0
INFLOW = np.array([15.0, 12.0, 10.0, 8.0, 12.0, 15.0, 18.0])
PRICE = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10])
DT = 86_400.0
HORIZON = 7

# Hydropower proxy (link m^3/s release to kWh via head and efficiency)
HEAD_M = 80.0
HEAD_GUIDE_REFERENCE_M = 30.0  # peer/guide magnitude for revenue comparison
ETA = 0.85
RHO = 1000.0
G = 9.81

ROOT = Path(__file__).resolve().parent


def day_energy_kwh_at_head(q_m3s: float, head_m: float) -> float:
    """Daily energy (kWh) at a given hydraulic head."""
    power_kw = ETA * RHO * G * head_m * q_m3s / 1000.0
    return power_kw * 24.0


def day_revenue_at_head(
    q_m3s: float, price_usd_per_kwh: float, head_m: float = HEAD_M
) -> float:
    return price_usd_per_kwh * day_energy_kwh_at_head(q_m3s, head_m)


def total_revenue_for_releases(
    releases: np.ndarray,
    prices: np.ndarray = PRICE,
    head_m: float = HEAD_M,
) -> float:
    releases = np.asarray(releases, dtype=float)
    return float(
        sum(day_revenue_at_head(releases[t], float(prices[t]), head_m) for t in range(len(releases)))
    )


def ecological_deficit_m3s_days(
    releases: np.ndarray, eco_flow_m3s: float = Q_ECO
) -> float:
    """Sum of daily max(0, Q_eco - Q_t) in (m^3/s)-day units."""
    releases = np.asarray(releases, dtype=float)
    return float(np.sum(np.maximum(0.0, eco_flow_m3s - releases)))


def daily_volume_m3(q_m3s: float) -> float:
    """Convert average flow (m^3/s) over one day to volume (m^3)."""
    return q_m3s * DT


def release_power_kw(q_m3s: float) -> float:
    """Hydropower power (kW) from release rate."""
    return ETA * RHO * G * HEAD_M * q_m3s / 1000.0


def day_energy_kwh(q_m3s: float) -> float:
    """Daily energy (kWh) from constant release over 24 h."""
    return day_energy_kwh_at_head(q_m3s, HEAD_M)


def day_revenue(q_m3s: float, price_usd_per_kwh: float) -> float:
    """Hydropower revenue for one day ($)."""
    return day_revenue_at_head(q_m3s, price_usd_per_kwh, HEAD_M)


def storage_after_day(
    storage_m3: float, inflow_m3s: float, release_m3s: float
) -> float:
    """Mass balance: V_{t+1} = V_t + (I - Q) * DT."""
    return storage_m3 + daily_volume_m3(inflow_m3s - release_m3s)


def storage_trajectory(
    releases: np.ndarray,
    initial_m3: float = V0,
    inflows: np.ndarray = INFLOW,
) -> np.ndarray:
    """End-of-day storage for each day (length n)."""
    releases = np.asarray(releases, dtype=float)
