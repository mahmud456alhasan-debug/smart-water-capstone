"""Public API for Streamlit reservoir tab."""

from __future__ import annotations

from typing import Any, Dict, List

from src.reservoir.optimizer import (
    ECO_FLOW_DEFAULT,
    optimize_horizon,
    validate_schedule,
)


def run_baseline_schedule(eco_flow_m3s: float = ECO_FLOW_DEFAULT) -> Dict[str, Any]:
    results, total = optimize_horizon(eco_flow_m3s=eco_flow_m3s)
    check = validate_schedule(results, eco_flow_m3s=eco_flow_m3s)
    rows = [
        {
            "day": r.day,
            "storage_start_mcm": r.storage_start_mcm,
            "inflow_m3s": r.inflow_m3s,
            "release_m3s": r.release_m3s,
            "storage_end_mcm": r.storage_end_mcm,
            "revenue_usd": r.revenue_usd,
        }
        for r in results
    ]
    return {
        "status": "ok",
        "total_revenue_usd": total,
        "validation": "PASS" if check["ok"] else "FAIL",
        "storage_slack_mcm": check["worst_storage_slack"],
        "schedule": rows,
    }
