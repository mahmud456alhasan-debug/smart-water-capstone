"""Data-loading utilities for CN lookup tables and rainfall event files."""

from __future__ import annotations

import os
from typing import NamedTuple

import pandas as pd


class CNLookup(NamedTuple):
    land_use: str
    cn: int
    description: str


def load_cn_lookup(path: str) -> pd.DataFrame:
    """Load the CN lookup CSV and validate its columns.

    Expected columns: ``land_use``, ``cn``, ``description``.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Cleaned lookup table with CN cast to int and validated in [1, 100].

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    ValueError
        If required columns are missing or any CN is out of range.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"CN lookup file not found: {path}")

    df = pd.read_csv(path)
    required = {"land_use", "cn", "description"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    df["cn"] = df["cn"].astype(int)
    invalid = df[(df["cn"] < 1) | (df["cn"] > 100)]
    if not invalid.empty:
        bad = invalid[["land_use", "cn"]].to_string(index=False)
        raise ValueError(f"CN values out of range [1, 100]:\n{bad}")

    return df


def load_rainfall_events(path: str) -> pd.DataFrame:
    """Load sample rainfall events CSV and validate columns.

    Expected columns: ``event_id``, ``watershed_id``, ``rainfall_mm``, ``land_use``.

    Parameters
    ----------
    path : str
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Event table with rainfall_mm validated >= 0.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    ValueError
        If required columns are missing or any rainfall value is negative.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Rainfall events file not found: {path}")

    df = pd.read_csv(path)
    required = {"event_id", "watershed_id", "rainfall_mm", "land_use"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    if (df["rainfall_mm"] < 0).any():
        raise ValueError("rainfall_mm must not contain negative values")

    return df
