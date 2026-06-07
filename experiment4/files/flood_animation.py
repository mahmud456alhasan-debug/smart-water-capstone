#!/usr/bin/env python3
"""
Rising-water flood animation with scientific overlay (Experiment 4 extra).

Creates flood_rise_animation.gif showing:
  - inundation depth map
  - water level, % flooded, and flood volume on each frame

More informative than a plain extent GIF (peer submissions often omit volume).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Sequence, Union

import numpy as np

from flood_inundation import (
    CELL_SIZE_M,
    flood_result,
    load_dem,
    ROOT,
)

DEFAULT_OUT = ROOT / "flood_rise_animation.gif"


def render_frame(
    dem: np.ndarray,
    level: float,
    dpi: int = 100,
) -> np.ndarray:
    """Return RGB array for one animation frame."""
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg

    res = flood_result(dem, level)
    fig, ax = plt.subplots(figsize=(5.5, 5), dpi=dpi)
    ax.imshow(dem, cmap="gray", origin="lower", vmin=dem.min(), vmax=dem.max())
    depth_ma = np.ma.masked_where(~res.flooded_mask, res.depth)
    vmax = max(0.5, float(res.depth.max()) if res.flooded_mask.any() else 1.0)
    ax.imshow(depth_ma, cmap="Blues", origin="lower", alpha=0.7, vmin=0, vmax=vmax)
    ax.set_title(
        f"Water level {level:.1f} m  |  "
        f"Flooded {res.percentage:.1f}%  |  "
        f"Volume {res.flood_volume_m3:,.0f} m³",
        fontsize=9,
    )
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.text(
        0.02, 0.98,
        f"Cell = {CELL_SIZE_M:.0f} m",
        transform=ax.transAxes, va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )
    fig.tight_layout()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = canvas.buffer_rgba()
    img = np.asarray(buf)[:, :, :3].copy()
    plt.close(fig)
    return img


def build_flood_animation(
    dem: np.ndarray,
    levels: Optional[Sequence[float]] = None,
    outpath: Union[str, Path] = DEFAULT_OUT,
    fps: float = 2.0,
) -> Path:
    """Write GIF from monotonically increasing water levels."""
    if levels is None:
        zmin, zmax = float(dem.min()), float(dem.max())
        levels = np.linspace(zmin + 2.0, zmax - 2.0, 16)

    frames: List[np.ndarray] = []
    for lv in levels:
        frames.append(render_frame(dem, float(lv)))

    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    try:
        import imageio.v2 as imageio
        imageio.mimsave(str(outpath), frames, duration=1.0 / fps)
    except Exception:
        from PIL import Image
        pil_frames = [Image.fromarray(f.astype(np.uint8)) for f in frames]
        pil_frames[0].save(
            outpath,
            save_all=True,
            append_images=pil_frames[1:],
            duration=int(1000 / fps),
            loop=0,
        )
    return outpath


def main() -> None:
    dem = load_dem(ROOT / "dem_data.npy")
    out = build_flood_animation(dem)
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
