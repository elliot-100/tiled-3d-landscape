"""Camera function."""

import math


def isometric_projection(
    world_x: float,
    world_y: float,
    world_z: float,
    display_x_offset: float = 0,
    display_y_offset: float = 0,
    scale_z: float = 1,
) -> tuple[float, float]:
    """Convert world (x, y, z) pixel coordinate to window (x, y) pixel coordinate.

    Uses 'video game isometric' projection, i.e. dimetric projection with a 2:1
    pixel ratio.

    Parameters
    ----------
    world_x: float
    world_y: float
    world_z: float
    display_x_offset: float = 0
        Optional screen pixel offset applied to result
    display_y_offset: float = 0
        Optional screen pixel offset applied to result
    scale_z: float = 1

    Returns
    -------
    Tuple[float, float]



    """
    display_x = (world_x - world_y) / math.sqrt(2)
    display_y = (world_x + world_y) / math.sqrt(2) / 2
    display_y += world_z * scale_z

    display_x += display_x_offset
    display_y += display_y_offset
    return display_x, display_y
