import random

import tcod as libtcod

from .game_map import GameMap
from . import tile_types


class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2

        return center_x, center_y

    @property
    def inner(self):
        ''' return the inner area of this room as a 2D array index '''
        return slice(self.x1 + 1, self.x2), (slice(self.y1 + 1, self.y2))

    def intersects(self, other):
        return all(
            (
                self.x1 <= other.x2,
                self.x2 >= other.x1,
                self.y1 <= other.y2,
                self.y2 >= other.y1,
            )
        )


def tunnel_between(start, end):
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        # move vertically then horizontally
        corner_x, corner_y = x1, y2

    # generate the coordinates for this tunnel
    for x, y in libtcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in libtcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(max_rooms, room_min_size, room_max_size, map_width, map_height, player):
    dungeon = GameMap(map_width, map_height)
    rooms = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # this room intersects, generate another

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:  # player starts in the first room
            player.x, player.y = new_room.center
        else:
            # dig a tunnel to prior room
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon
