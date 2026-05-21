"""Load rainfall series from CSV."""

from __future__ import annotations

import pandas as pd


def load_rainfall_csv(path: str) -> pd.DataFrame:
    """Return DataFrame with columns datetime, rainfall_mm."""
    df = pd.read_csv(path, parse_dates=["datetime"])
    required = {"datetime", "rainfall_mm"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain {required}")
    return df.sort_values("datetime")
