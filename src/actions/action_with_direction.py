"""Action with direction for movement and targeting."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base_action import Action

if TYPE_CHECKING:
    from entity.actor import Actor
    from entity.base_entity import Entity
    from game_types import Position


class ActionWithDirection(Action):
    """An action that targets a direction relative to the entity."""

    def __init__(self, entity: Actor, dx: int, dy: int) -> None:
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Position:
        """Return the destination position of this action."""
        return (self.entity.x + self.dx, self.entity.y + self.dy)

    @property
    def blocking_entity(self) -> Entity | None:
        """Return the blocking entity at this action's destination."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Actor | None:
        """Return the actor at this action's destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        """Perform this action. Must be overridden by subclasses."""
        raise NotImplementedError()
