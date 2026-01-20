"""Base entity class for all game objects."""

from __future__ import annotations

import copy
import math
from typing import TYPE_CHECKING

from render_order import RenderOrder

if TYPE_CHECKING:
    from game_types import ColorRGB, Position
    from map_objects.game_map import GameMap


class Entity:
    """A generic object to represent players, enemies, items, etc."""

    parent: GameMap | None

    def __init__(
        self,
        parent: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        icon: str = '?',
        color: ColorRGB = (255, 255, 255),
        name: str = '<Unnamed>',
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ) -> None:
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def position(self) -> Position:
        """Return the entity's current position as a tuple."""
        return (self.x, self.y)

    def spawn(self, gamemap: GameMap, x: int, y: int) -> Entity:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: GameMap | None = None) -> None:
        """Place this entity at a new location, optionally on a new game map."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, 'parent') and self.parent is self.gamemap:
                self.gamemap.entities.discard(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """Return the distance from this entity to the given coordinates."""
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        """Move the entity by the given amount."""
        self.x += dx
        self.y += dy
