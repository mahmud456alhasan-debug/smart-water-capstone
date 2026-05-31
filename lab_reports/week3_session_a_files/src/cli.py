"""Command-line interface for SCS-CN runoff analysis."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.data_loader import load_cn_lookup, load_rainfall_events
from src.scs_cn import calculate_runoff, calculate_runoff_series, summarize_runoff
from src.visualization import plot_runoff_by_land_use, plot_runoff_vs_rainfall


def _resolve_data_path(filename: str) -> str:
    return str(Path(__file__).resolve().parent.parent / "data" / filename)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="SCS-CN runoff calculator for flood-risk screening.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # single ─────────────────────────────────────────────────────────────────
    single = sub.add_parser("single", help="Single (P, CN) pair")
    single.add_argument("P", type=float, help="Rainfall depth (mm)")
    single.add_argument("CN", type=float, help="Curve number [1, 100]")

    # batch ──────────────────────────────────────────────────────────────────
    batch = sub.add_parser("batch", help="Run all events from sample_rainfall.csv")
    batch.add_argument(
        "--cn-lookup",
        default=_resolve_data_path("cn_lookup.csv"),
        help="Path to CN lookup CSV",
    )
    batch.add_argument(
        "--rainfall",
        default=_resolve_data_path("sample_rainfall.csv"),
        help="Path to rainfall events CSV",
    )

    # table ──────────────────────────────────────────────────────────────────
    table = sub.add_parser("table", help="Print summary table for a range")
    table.add_argument("P", type=float, help="Rainfall depth (mm)")
    table.add_argument(
        "CN_values",
        type=int,
        nargs="+",
        help="One or more CN values",
    )
    table.add_argument("--labels", nargs="*", help="Optional per-CN labels")

    # plot ───────────────────────────────────────────────────────────────────
    plt_cmd = sub.add_parser("plot", help="Plot runoff curves")
    plt_cmd.add_argument(
        "--max-P",
        type=float,
        default=150.0,
        help="Maximum rainfall for plot (mm)",
    )
    plt_cmd.add_argument(
        "--CN",
        type=int,
        nargs="+",
        default=[70, 80, 90, 98],
        help="CN curves to plot",
    )
    plt_cmd.add_argument(
        "--output",
        "-o",
        default=None,
        help="Save plot to file instead of showing",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "single":
        Q = calculate_runoff(args.P, args.CN)
        print(f"P = {args.P:.1f} mm, CN = {args.CN:.0f}  ->  Q = {Q:.2f} mm")
        return 0

    if args.command == "batch":
        cn_df = load_cn_lookup(args.cn_lookup)
        rain_df = load_rainfall_events(args.rainfall)

        merged = rain_df.merge(cn_df, on="land_use", how="left")
        if merged["cn"].isna().any():
            missing = merged.loc[merged["cn"].isna(), "land_use"].unique()
            print(f"WARNING: No CN for land use(s): {list(missing)}", file=sys.stderr)

        merged["Q (mm)"] = calculate_runoff_series(
            merged["rainfall_mm"].values,
            merged["cn"].values,
        )
        print(merged.to_string(index=False))
        return 0

    if args.command == "table":
        labels = args.labels if args.labels else None
        P_arr = [args.P] * len(args.CN_values)
        df = summarize_runoff(P_arr, args.CN_values, labels=labels)
        print(df.to_string(index=False))
        return 0

    if args.command == "plot":
        import numpy as np

        P = np.linspace(0, args.max_P, 200)
        fig = plot_runoff_vs_rainfall(P, args.CN)
        if args.output:
            fig.savefig(args.output, dpi=150)
            print(f"Plot saved to {args.output}")
        else:
            plt.show()
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
