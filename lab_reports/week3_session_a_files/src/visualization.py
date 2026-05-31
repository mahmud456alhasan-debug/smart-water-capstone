"""Visualization components for SCS-CN runoff analysis."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_runoff_vs_rainfall(
    P_values: np.ndarray,
    CN_values: list[int] | np.ndarray,
    ax: plt.Axes | None = None,
    title: str = "SCS-CN Runoff vs Rainfall",
) -> plt.Figure:
    """Plot runoff depth Q against rainfall P for one or more CN curves.

    Parameters
    ----------
    P_values : np.ndarray
        1-D array of rainfall depths (mm) to evaluate.
    CN_values : list of int or np.ndarray
        Curve numbers to plot.
    ax : plt.Axes, optional
        Matplotlib axes to draw on.  A new figure+axes is created if not provided.
    title : str
        Plot title.

    Returns
    -------
    plt.Figure
        The figure handle.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    else:
        fig = ax.figure

    P = np.asarray(P_values, dtype=float)

    for CN in CN_values:
        S = 25400.0 / CN - 254.0
        Ia = 0.2 * S
        Q = np.where(
            P > Ia,
            (P - Ia) ** 2 / (P - Ia + S),
            0.0,
        )
        ax.plot(P, Q, label=f"CN = {CN}")

    ax.plot(P, P, "k--", alpha=0.4, label="Q = P (upper bound)")
    ax.set_xlabel("Rainfall P (mm)")
    ax.set_ylabel("Runoff Q (mm)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_runoff_by_land_use(
    df: pd.DataFrame,
    ax: plt.Axes | None = None,
    title: str = "Runoff by Land Use",
) -> plt.Figure:
    """Bar chart of runoff depth per land-use category.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns ``land_use`` (or ``label``) and ``Q (mm)``.
        Typically the output of :func:`src.scs_cn.summarize_runoff`.
    ax : plt.Axes, optional
    title : str

    Returns
    -------
    plt.Figure
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    else:
        fig = ax.figure

    label_col = "land_use" if "land_use" in df.columns else "label"
    x = df[label_col].astype(str)
    y = df["Q (mm)"]

    bars = ax.bar(x, y, color="steelblue", edgecolor="black")
    ax.bar_label(bars, fmt="%.1f", padding=2)
    ax.set_xlabel("Land Use")
    ax.set_ylabel("Runoff Q (mm)")
    ax.set_title(title)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig
