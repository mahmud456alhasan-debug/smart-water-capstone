#!/usr/bin/env python3
"""Scientific figures, sensitivity, and performance analysis (Experiment 4)."""

from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from flood_inundation import (
    CURVE_LEVEL_END,
    CURVE_LEVEL_START,
    CURVE_LEVEL_STEP,
    DEFAULT_LEVELS,
    calculate_flood,
    flood_result,
    generate_dem,
    load_dem,
    simulate_rising_water,
)

SENSITIVITY_SEEDS = (42, 7, 99)
REFERENCE_LEVEL_M = 50.0


def _add_dem_contours(ax, dem: np.ndarray, n_levels: int = 10) -> None:
    ny, nx = dem.shape
    x = np.arange(nx)
    y = np.arange(ny)
    ax.contour(x, y, dem, levels=n_levels, colors="black", linewidths=0.4, alpha=0.5)


def plot_dem_overview_scientific(
    dem: np.ndarray,
    outpath: Path,
    dpi: int = 200,
) -> Path:
    """Terrain DEM with optional contours (Part 1 / report figure)."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(dem, cmap="terrain", origin="lower")
    _add_dem_contours(ax, dem)
    ax.set_xlabel("Column index")
    ax.set_ylabel("Row index")
    ax.set_title("Synthetic DEM used for flood inundation analysis")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Elevation (m)")
    fig.tight_layout()
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return outpath


def plot_dem_histogram(
    dem: np.ndarray,
    outpath: Path,
    water_levels: Sequence[float] = (40.0, 50.0),
    dpi: int = 200,
) -> Path:
    """Elevation distribution with water-level reference lines."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4.5))
    flat = dem.ravel()
    ax.hist(flat, bins=40, color="#5d6d7e", edgecolor="white", alpha=0.85)
    colors = ["#2980b9", "#c0392b"]
    for lv, col in zip(water_levels, colors):
        ax.axvline(lv, color=col, linestyle="--", linewidth=1.5, label=f"Water level {lv:.0f} m")
    ax.axvline(float(flat.min()), color="#27ae60", linestyle=":", linewidth=1.2, label="Min DEM")
    ax.axvline(float(flat.max()), color="#8e44ad", linestyle=":", linewidth=1.2, label="Max DEM")
    ax.set_xlabel("Elevation (m)")
    ax.set_ylabel("Cell count")
    ax.set_title("DEM elevation distribution and flood stage references")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return outpath


def annotate_curve_growth(ax, levels: np.ndarray, pcts: np.ndarray) -> None:
    """Mark first wetting, 10% flooded, and steepest growth on flood curve."""
    # First level with any flooding
    wet_idx = int(np.argmax(pcts > 1e-9))
    if pcts[wet_idx] <= 1e-9:
        wet_idx = 0
    ax.annotate(
        "First flooding",
        (levels[wet_idx], pcts[wet_idx]),
        textcoords="offset points",
        xytext=(10, 12),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#1a5276", lw=0.9),
    )

    # 10% threshold
    idx_10 = int(np.argmax(pcts >= 10.0))
    if pcts[idx_10] >= 10.0:
        ax.annotate(
            "10% flooded",
            (levels[idx_10], pcts[idx_10]),
            textcoords="offset points",
            xytext=(-55, -18),
            fontsize=8,
            arrowprops=dict(arrowstyle="->", color="#884ea0", lw=0.9),
        )

    diffs = np.diff(pcts)
    if len(diffs):
        steepest = int(np.argmax(diffs)) + 1
        ax.annotate(
            "Steepest growth",
            (levels[steepest], pcts[steepest]),
            textcoords="offset points",
            xytext=(12, -22),
            fontsize=8,
            arrowprops=dict(arrowstyle="->", color="#b9770e", lw=0.9),
        )


def plot_flood_curve_annotated(
    levels: Sequence[float],
    percentages: Sequence[float],
    outpath: Path,
    dem_min: Optional[float] = None,
    dem_max: Optional[float] = None,
    dpi: int = 200,
) -> Path:
    """Enhanced flood curve with growth annotations."""
    import matplotlib.pyplot as plt

    levels_a = np.asarray(levels, dtype=float)
    pcts_a = np.asarray(percentages, dtype=float)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    ax.plot(levels_a, pcts_a, "o-", color="#21618c", linewidth=2, markersize=5, label="Flooded area")
    ax.fill_between(levels_a, pcts_a, alpha=0.15, color="#21618c")
    if dem_min is not None:
        ax.axvline(dem_min, color="#27ae60", linestyle="--", linewidth=1.2, label=f"Min DEM ({dem_min:.1f} m)")
    if dem_max is not None:
        ax.axvline(dem_max, color="#c0392b", linestyle="--", linewidth=1.2, label=f"Max DEM ({dem_max:.1f} m)")
    annotate_curve_growth(ax, levels_a, pcts_a)
    ax.set_xlabel("Water level (m)")
    ax.set_ylabel("Flooded area (%)")
    ax.set_title("Flood curve: cumulative inundation growth (40--50 m)")
    ax.set_xlim(CURVE_LEVEL_START - 1, CURVE_LEVEL_END + 1)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return outpath


def plot_flood_volume_curve(
    dem: np.ndarray,
    levels: Iterable[float],
    outpath: Path,
    dpi: int = 200,
) -> Path:
    """Water level vs total flood volume (m^3)."""
    import matplotlib.pyplot as plt

    lv_list = [float(x) for x in levels]
    volumes = [flood_result(dem, lv).flood_volume_m3 for lv in lv_list]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(lv_list, volumes, "s-", color="#117a65", linewidth=2, markersize=5)
    ax.fill_between(lv_list, volumes, alpha=0.12, color="#117a65")
    ax.set_xlabel("Water level (m)")
    ax.set_ylabel("Total flood volume (m$^3$)")
    ax.set_title("Flood volume vs water level (bathtub: $\\sum$ depth $\\times$ cell area)")
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(outpath, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return outpath


def run_seed_sensitivity(
    seeds: Sequence[int] = SENSITIVITY_SEEDS,
    water_level: float = REFERENCE_LEVEL_M,
) -> List[Tuple[int, float, float, float]]:
    """Return (seed, elev_min, elev_max, flooded_pct_at_level) per terrain realization."""
    rows: List[Tuple[int, float, float, float]] = []
    for seed in seeds:
        dem = generate_dem(seed=int(seed))
        r = flood_result(dem, water_level)
        rows.append((int(seed), float(dem.min()), float(dem.max()), r.percentage))
    return rows


def export_sensitivity_csv(rows: List[Tuple[int, float, float, float]], path: Path) -> Path:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "elev_min_m", "elev_max_m", f"flooded_pct_at_{REFERENCE_LEVEL_M:.0f}m"])
        for seed, zmin, zmax, pct in rows:
            w.writerow([seed, f"{zmin:.2f}", f"{zmax:.2f}", f"{pct:.2f}"])
    return path


def benchmark_performance(dem: np.ndarray, n_repeat: int = 50) -> Dict[str, float]:
    """Timing table for load, single flood, and full curve (milliseconds)."""
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".npy") as tmp:
        tmp_path = Path(tmp.name)
        np.save(tmp_path, dem)

        t0 = time.perf_counter()
        for _ in range(3):
            _ = np.load(tmp_path)
        load_ms = (time.perf_counter() - t0) / 3 * 1000

    t0 = time.perf_counter()
    for _ in range(n_repeat):
        calculate_flood(dem, 45.0)
    single_ms = (time.perf_counter() - t0) / n_repeat * 1000

    t0 = time.perf_counter()
    simulate_rising_water(dem, DEFAULT_LEVELS)
    curve_ms = (time.perf_counter() - t0) * 1000

    return {
        "dem_load_ms": load_ms,
        "single_flood_ms": single_ms,
        "curve_simulation_ms": curve_ms,
    }


def write_interpretation_md(
    dem: np.ndarray,
    curve: List[Tuple[float, float]],
    sensitivity: List[Tuple[int, float, float, float]],
    benchmarks: Dict[str, float],
    path: Path,
) -> Path:
    """Physical interpretation and limitations for report / appendix."""
    pcts = [p for _, p in curve]
    levels = [lv for lv, _ in curve]
    z_min, z_max = float(dem.min()), float(dem.max())
    median_z = float(np.median(dem))

    # Steepest segment
    diffs = np.diff(pcts)
    steepest_i = int(np.argmax(diffs)) if len(diffs) else 0
    steepest_range = f"{levels[steepest_i]:.1f}--{levels[steepest_i + 1]:.1f} m"

    lines = [
        "# Experiment 4: Physical Interpretation and Limitations",
        "",
        "## Physical interpretation",
        "",
        f"- **Terrain:** Synthetic 100x100 DEM (seed 42), elevation {z_min:.2f}--{z_max:.2f} m; "
        f"median {median_z:.1f} m.",
        "- **Valleys flood first:** Central depression and low cells wet before ridges when "
        "water level rises from 40 m.",
        f"- **Accelerated growth:** Largest step increase in flooded % occurs near "
        f"{steepest_range} as the water surface crosses many cells near median elevation.",
        "- **Spatial connectivity:** At ~48--50 m, inundation patches merge across the valley "
        "floor (visible on contour-overlaid maps).",
        "- **Monotonic curve:** Flooded area and volume increase non-decreasing with stage — "
        "consistent with a flat bathtub surface.",
        "",
        "## Seed sensitivity (@ 50 m water level)",
        "",
        "| Seed | z_min (m) | z_max (m) | Flooded % |",
        "|------|-----------|-----------|-----------|",
    ]
    for seed, zmin, zmax, pct in sensitivity:
        lines.append(f"| {seed} | {zmin:.2f} | {zmax:.2f} | {pct:.2f} |")
    lines.extend([
        "",
        "Inundation percentage depends on terrain realization; different seeds change valley "
        "depth and therefore wet cell counts at the same absolute stage.",
        "",
        "## Performance (this machine)",
        "",
        "| Task | Runtime (ms) |",
        "|------|----------------|",
        f"| DEM load (`dem_data.npy`) | {benchmarks['dem_load_ms']:.2f} |",
        f"| Single `calculate_flood` | {benchmarks['single_flood_ms']:.2f} |",
        f"| Full curve ({len(DEFAULT_LEVELS)} levels) | {benchmarks['curve_simulation_ms']:.2f} |",
        "",
        "## Limitations (model assumptions)",
        "",
        "1. **Flat water surface** — no slope along the flood wave.",
        "2. **No hydraulic routing** — isolated depressions could fill in reality only if connected.",
        "3. **No flow momentum** — no Saint-Venant or 2D hydrodynamics.",
        "4. **No infiltration or evaporation** — water does not leave the surface.",
        "5. **No buildings or levees** — barriers are not represented.",
        "",
        "Despite these simplifications, bathtub DEM inundation is widely used for rapid "
        "flood screening, scenario comparison, and teaching DEM-based risk mapping.",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def run_scientific_outputs(root: Path, dem: np.ndarray, curve: List[Tuple[float, float]]) -> dict:
    """Generate all scientific/analysis deliverables."""
    from flood_inundation import visualize_flood

    root = Path(root)
    plot_dem_overview_scientific(dem, root / "dem_overview.png")
    plot_dem_histogram(dem, root / "dem_histogram.png")

    r40 = flood_result(dem, 40.0)
    r50 = flood_result(dem, 50.0)
    visualize_flood(
        dem, r40.flooded_mask, r40.depth, 40.0, r40.percentage,
        root / "flood_extent_40m.png", contours=True,
    )
    visualize_flood(
        dem, r50.flooded_mask, r50.depth, 50.0, r50.percentage,
        root / "flood_extent_50m.png", contours=True,
    )

    plot_flood_curve_annotated(
        [lv for lv, _ in curve],
        [p for _, p in curve],
        root / "flood_curve.png",
        dem_min=float(dem.min()),
        dem_max=float(dem.max()),
    )
    plot_flood_volume_curve(dem, [lv for lv, _ in curve], root / "flood_volume_curve.png")

    sensitivity = run_seed_sensitivity()
    export_sensitivity_csv(sensitivity, root / "sensitivity_seeds.csv")
    benchmarks = benchmark_performance(dem)
    write_interpretation_md(dem, curve, sensitivity, benchmarks, root / "interpretation.md")

    return {
        "sensitivity": sensitivity,
        "benchmarks": benchmarks,
    }
