"""Tile type definitions for the game map."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from game_types import ColorRGB

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ('ch', np.int32),  # Unicode codepoint
        ('fg', '3B'),      # 3 unsigned bytes for RGB colors
        ('bg', '3B'),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ('walkable', np.bool_),     # True if this tile can be walked over
        ('transparent', np.bool_),  # True if this tile doesn't block FOV
        ('dark', graphic_dt),       # Graphics when tile is not in FOV
        ('light', graphic_dt),      # Graphics when tile is in FOV
    ]
)


def new_tile(
    *,
    walkable: bool,
    transparent: bool,
    dark: tuple[int, ColorRGB, ColorRGB],
    light: tuple[int, ColorRGB, ColorRGB],
) -> np.ndarray:
    """Create a new tile type with the given properties."""
    return np.array(
        (walkable, transparent, dark, light),
        dtype=tile_dt,
    )


# FOW - fog of war (unseen tiles)
FOW = np.array(
    (ord(' '), (255, 255, 255), (0, 0, 0)),
    dtype=graphic_dt,
)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(' '), (255, 255, 255), (50, 50, 150)),
    light=(ord(' '), (255, 255, 255), (255, 242, 150)),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(' '), (255, 255, 255), (0, 0, 100)),
    light=(ord(' '), (255, 255, 255), (236, 207, 83)),
)
