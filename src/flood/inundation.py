"""Flood mask and depth — stub; copy logic from week6_session_b_lab4 in Session B."""

from __future__ import annotations

import numpy as np
from typing import Tuple


def simulate_flood(dem: np.ndarray, flood_level: float) -> Tuple[np.ndarray, np.ndarray]:
    """Wet if elevation <= flood_level; depth zero elsewhere."""
    flooded_mask = dem <= flood_level
    depth = np.maximum(0.0, flood_level - dem)
    depth = np.where(flooded_mask, depth, 0.0)
    return flooded_mask, depth
