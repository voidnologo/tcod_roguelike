import numpy as np
from map_objects import tile_types


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = np.full(
            (self.width, self.height),
            fill_value=tile_types.wall,
            order='F',
        )

        tiles[30:33, 22] = tile_types.wall
        return tiles

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        console.tiles_rgb[0 : self.width, 0 : self.height] = self.tiles['dark']  # noqa: E203
