"""Base action class for all game actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity.actor import Actor


class Action:
    """Base class for all actions that can be performed by entities."""

    def __init__(self, entity: Actor) -> None:
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action's entity belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action. Must be overridden by subclasses."""
        raise NotImplementedError()
