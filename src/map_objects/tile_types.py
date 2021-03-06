import numpy as np


# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ('ch', np.int32),  # Unicode codepoint.
        ('fg', '3B'),  # 3 unsigned bytes, for RGB colors.
        ('bg', '3B'),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ('walkable', np.bool),  # True if this tile can be walked over.
        ('transparent', np.bool),  # True if this tile doesn't block FOV.
        ('dark', graphic_dt),  # Graphics for when this tile is not in FOV.
        ('light', graphic_dt),  # Graphics for when this tile is in FOV.
    ]
)


def new_tile(*, walkable, transparent, dark, light):
    return np.array(
        (
            walkable,
            transparent,
            dark,
            light,
        ),
        dtype=tile_dt,
    )


# FOW - fog of war
FOW = np.array(
    (
        ord(' '),
        (255, 255, 255),
        (0, 0, 0),
    ),
    dtype=graphic_dt,
)


floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(
        ord(' '),
        (255, 255, 255),
        (50, 50, 150),
    ),
    light=(
        ord(' '),
        (255, 255, 255),
        (255, 242, 150),
    ),
)

wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(
        ord(' '),
        (255, 255, 255),
        (0, 0, 100),
    ),
    light=(
        ord(' '),
        (255, 255, 255),
        (236, 207, 83),
    ),
)
