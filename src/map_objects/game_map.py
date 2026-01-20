"""Game map and dungeon floor management."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING

import numpy as np

from entity import Actor, Item
from map_objects import tile_types

if TYPE_CHECKING:
    from tcod.console import Console

    from engine import Engine
    from entity.base_entity import Entity


class GameMap:
    """Represents a single floor of the dungeon."""

    def __init__(
        self,
        engine: Engine,
        width: int,
        height: int,
        entities: list[Entity],
    ) -> None:
        self.engine = engine
        self.width = width
        self.height = height
        self.entities: set[Entity] = set(entities)
        self.tiles = self._initialize_tiles()

        self.visible = np.full((width, height), fill_value=False, order='F')
        self.explored = np.full((width, height), fill_value=False, order='F')

    @property
    def gamemap(self) -> GameMap:
        """Return self for compatibility with entity parent attribute."""
        return self

    def _initialize_tiles(self) -> np.ndarray:
        """Create initial tile array filled with walls."""
        tiles = np.full(
            (self.width, self.height),
            fill_value=tile_types.wall,
            order='F',
        )
        tiles[30:33, 22] = tile_types.wall
        return tiles

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if the coordinates are within map bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """Render the map and entities to the console."""
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles['light'], self.tiles['dark']],
            default=tile_types.FOW,
        )

        for entity in sorted(self.entities, key=lambda x: x.render_order.value):
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.icon, fg=entity.color)

    def get_entities_at(
        self,
        x: int,
        y: int,
        entity_type: type[Entity] | None = None,
    ) -> Iterator[Entity]:
        """Yield all entities at the given position, optionally filtered by type."""
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                if entity_type is None or isinstance(entity, entity_type):
                    yield entity

    def get_blocking_entity_at_location(self, x: int, y: int) -> Entity | None:
        """Return the blocking entity at the given location, if any."""
        for entity in self.entities:
            if entity.blocks_movement and entity.x == x and entity.y == y:
                return entity
        return None

    def get_actor_at_location(self, x: int, y: int) -> Actor | None:
        """Return the living actor at the given location, if any."""
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over all living actors on the map."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        """Iterate over all items on the map."""
        yield from (entity for entity in self.entities if isinstance(entity, Item))
