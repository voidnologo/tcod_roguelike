"""Procedural dungeon generation."""

from __future__ import annotations

import random
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

import tcod.los

import entity_factories
from map_objects import tile_types
from map_objects.game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine
    from entity.base_entity import Entity
    from game_types import Position


@dataclass(frozen=True, slots=True)
class SpawnEntry:
    """An entry in a spawn table with a factory and weight."""

    factory: Entity
    weight: float


MONSTER_SPAWN_TABLE: list[SpawnEntry] = [
    SpawnEntry(entity_factories.orc, 0.8),
    SpawnEntry(entity_factories.troll, 0.2),
]

ITEM_SPAWN_TABLE: list[SpawnEntry] = [
    SpawnEntry(entity_factories.health_potion, 0.7),
    SpawnEntry(entity_factories.fireball_scroll, 0.1),
    SpawnEntry(entity_factories.confusion_scroll, 0.1),
    SpawnEntry(entity_factories.lightning_scroll, 0.1),
]


def weighted_choice(table: list[SpawnEntry]) -> Entity:
    """Select a random entry from a spawn table based on weights."""
    total = sum(entry.weight for entry in table)
    roll = random.random() * total
    cumulative = 0.0
    for entry in table:
        cumulative += entry.weight
        if roll < cumulative:
            return entry.factory
    return table[-1].factory


@dataclass(slots=True)
class RectangularRoom:
    """A rectangular room on the map."""

    x: int
    y: int
    width: int
    height: int

    @property
    def x1(self) -> int:
        return self.x

    @property
    def y1(self) -> int:
        return self.y

    @property
    def x2(self) -> int:
        return self.x + self.width

    @property
    def y2(self) -> int:
        return self.y + self.height

    @property
    def center(self) -> Position:
        """Return the center coordinates of the room."""
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    @property
    def inner(self) -> tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return (slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2))

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another room."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


def tunnel_between(start: Position, end: Position) -> Iterator[Position]:
    """Generate an L-shaped tunnel between two points."""
    x1, y1 = start
    x2, y2 = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def place_entities(
    room: RectangularRoom,
    dungeon: GameMap,
    max_monsters: int,
    max_items: int,
) -> None:
    """Place random monsters and items in a room."""
    num_monsters = random.randint(0, max_monsters)
    num_items = random.randint(0, max_items)

    for _ in range(num_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(e.x == x and e.y == y for e in dungeon.entities):
            monster = weighted_choice(MONSTER_SPAWN_TABLE)
            monster.spawn(dungeon, x, y)

    for _ in range(num_items):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(e.x == x and e.y == y for e in dungeon.entities):
            item = weighted_choice(ITEM_SPAWN_TABLE)
            item.spawn(dungeon, x, y)


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    max_items_per_room: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])
    rooms: list[RectangularRoom] = []

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other) for other in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for tunnel_x, tunnel_y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[tunnel_x, tunnel_y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room, max_items_per_room)
        rooms.append(new_room)

    return dungeon
