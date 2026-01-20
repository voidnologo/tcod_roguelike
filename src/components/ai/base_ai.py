"""Base AI component for entity behavior."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import tcod.path

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.actor import Actor
    from game_types import Position


class BaseAI(BaseComponent):
    """Base class for AI components that control actor behavior."""

    entity: Actor

    def __init__(self, entity: Actor) -> None:
        self.entity = entity

    @property
    def parent(self) -> Actor:
        """Alias for entity to maintain BaseComponent compatibility."""
        return self.entity

    def perform(self) -> None:
        """Perform the AI's action. Must be overridden by subclasses."""
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> list[Position]:
        """Compute a path from the entity to the destination."""
        cost = np.array(self.entity.gamemap.tiles['walkable'], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        return [(index[0], index[1]) for index in path]
