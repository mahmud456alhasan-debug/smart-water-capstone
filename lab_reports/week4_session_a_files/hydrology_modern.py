#!/usr/bin/env python3
"""Modernised watershed runoff calculator.

Replaces the callback-style legacy_hydrology.py with:
- Type hints (Python 3.8 compatible using Union/Optional)
- async/await I/O via asyncio + thread pool executor
- Extracted functions, no global mutable state
- NumPy vectorised batch runoff computation
- Comprehensive error handling with meaningful messages
"""

import asyncio
import csv
import sys
from typing import Dict, List, Optional, Tuple, Union

import numpy as np

# --- Constants ---

LAND_USE_CN: Dict[str, int] = {
    "forest": 70,
    "pasture": 80,
    "cultivated": 85,
    "residential": 90,
    "paved": 98,
}

DEFAULT_CN: int = 80
RAINFALL_URL: str = "https://httpbin.org/bytes/8"
HTTP_TIMEOUT: float = 2.0

RowTuple = Tuple[str, str, float, str, int, float]


# --- Core hydrology functions ---

def compute_s(cn: int) -> float:
    """Compute maximum potential retention S (mm) from curve number."""
    return 25400.0 / cn - 254.0


def initial_abstraction(s: float) -> float:
    """Compute initial abstraction Ia = 0.2S."""
    return 0.2 * s


def scs_runoff(rainfall_mm: float, cn: int) -> float:
    """Compute SCS Curve Number runoff depth Q (mm).

    Args:
        rainfall_mm: Rainfall depth in mm.
        cn: Curve number (30–100).

    Returns:
        Runoff depth in mm, capped at rainfall_mm.
    """
    if rainfall_mm <= 0:
        return 0.0
    s = compute_s(cn)
    ia = initial_abstraction(s)
    if rainfall_mm <= ia:
        return 0.0
    numerator = (rainfall_mm - ia) ** 2
    denominator = rainfall_mm - ia + s
    q = numerator / denominator
    return min(q, rainfall_mm)


def cn_for_land_use(land_use: str) -> int:
    """Return curve number for a given land-use type.

    Falls back to DEFAULT_CN (80) for unrecognised types.
    """
    return LAND_USE_CN.get(land_use, DEFAULT_CN)


def batch_runoff(rainfall_mm: np.ndarray, cn: np.ndarray) -> np.ndarray:
    """Vectorised SCS runoff over numpy arrays.

    Args:
        rainfall_mm: 1-D array of rainfall depths.
        cn: 1-D array of curve numbers (same length).

    Returns:
        Array of runoff depths, element-wise capped at rainfall_mm.
    """
    s = 25400.0 / cn - 254.0
    ia = 0.2 * s
    q = np.where(
        rainfall_mm <= ia,
        0.0,
        (rainfall_mm - ia) ** 2 / (rainfall_mm - ia + s),
    )
    return np.minimum(q, rainfall_mm)


# --- I/O ---

async def fetch_rainfall_async(url: str, timeout: float = HTTP_TIMEOUT) -> Optional[float]:
    """Fetch a rainfall reading from a URL asynchronously.

    Uses a thread-pool executor to avoid blocking the event loop.
    Returns the parsed float, or None on any failure (network,
    HTTP error, bad payload).
    """
    import urllib.request

    loop = asyncio.get_running_loop()

    def _fetch() -> Optional[float]:
        try:
            with urllib.request.urlopen(url, timeout=timeout) as resp:
                raw = resp.read()
            return float(raw.decode().strip())
        except (OSError, ValueError, TypeError):
            return None

    return await loop.run_in_executor(None, _fetch)


def read_events(path: str) -> List[Dict[str, Union[str, float]]]:
    """Parse a CSV event file into a list of dictionaries.

    Expected columns: event_id, watershed_id, rainfall_mm, land_use.
    Raises on missing or malformed files.
    """
    events: List[Dict[str, Union[str, float]]] = []
    try:
        with open(path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                events.append(
                    {
                        "event_id": row["event_id"],
                        "watershed_id": row["watershed_id"],
                        "rainfall_mm": float(row["rainfall_mm"]),
                        "land_use": row["land_use"],
                    }
                )
    except (IOError, OSError, ValueError, KeyError) as exc:
        print(f"Failed to read events from {path}: {exc}", file=sys.stderr)
        raise
    return events


# --- Reporting ---

def print_report(rows: List[RowTuple], total_q: float) -> None:
    """Print a formatted runoff report matching legacy output exactly."""
    print("=== LEGACY RUNOFF REPORT ===")
    print("event  watershed  P_mm  land_use  CN  Q_mm")
    for eid, ws, p, lu, cn, q in rows:
        print(
            "%5s  %9s  %5.1f  %10s  %2d  %8.4f"
            % (eid, ws, p, lu, cn, q)
        )
    print("TOTAL Q =", total_q)


# --- Orchestration ---

async def _process_async(path: str) -> None:
    """Async pipeline: read events, fetch all rainfall concurrently, compute vectorised."""
    events = read_events(path)

    # Concurrent I/O phase
    tasks = [fetch_rainfall_async(RAINFALL_URL) for _ in events]
    api_results: List[Optional[float]] = await asyncio.gather(*tasks)

    # Build data arrays
    p_uses: List[float] = []
    cns: List[int] = []
    for ev, p_api in zip(events, api_results):
        p_csv = float(ev["rainfall_mm"])  # type: ignore[arg-type]
        p_use = p_api if p_api is not None else p_csv
        p_uses.append(p_use)
        cns.append(cn_for_land_use(str(ev["land_use"])))

    # Vectorised runoff computation
    qs = batch_runoff(np.array(p_uses, dtype=np.float64),
                      np.array(cns, dtype=np.int64))

    # Assemble results
    results: List[RowTuple] = []
    total_q: float = 0.0
    for ev, p_use, cn, q in zip(events, p_uses, cns, qs):
        q_val = float(q)
        results.append((
            str(ev["event_id"]),
            str(ev["watershed_id"]),
            p_use,
            str(ev["land_use"]),
            cn,
            q_val,
        ))
        total_q += q_val

    print_report(results, total_q)


def process(path: str) -> None:
    """Synchronous entry point wrapping the async pipeline."""
    try:
        asyncio.run(_process_async(path))
    except Exception as exc:
        print(f"Pipeline failed: {exc}", file=sys.stderr)
        raise


# --- CLI ---

def main() -> None:
    """CLI entry point."""
    path = "data/events.csv"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    process(path)


if __name__ == "__main__":
    main()
