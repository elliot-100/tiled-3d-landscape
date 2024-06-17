"""Camera function."""

import math
from typing import Tuple


def camera(
    world_x: float,
    world_y: float,
    world_height: float,
    window_width: int,
    height_scale: float,
) -> Tuple[float, float]:
    """Convert world coordinate (pixels) to window coordinate."""
    x = (world_x - world_y) / math.sqrt(2) + window_width / 2
    y = (world_x + world_y) / math.sqrt(2) / 2 + 100
    y += world_height * height_scale
    return x, y
