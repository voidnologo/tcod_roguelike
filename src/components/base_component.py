"""Base component class for entity components."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity.actor import Actor
    from map_objects.game_map import GameMap


class BaseComponent:
    """Base class for all entity components."""

    parent: Actor

    @property
    def engine(self) -> Engine:
        """Return the engine this component's parent belongs to."""
        return self.gamemap.engine

    @property
    def gamemap(self) -> GameMap:
        """Return the game map this component's parent belongs to."""
        return self.parent.gamemap
