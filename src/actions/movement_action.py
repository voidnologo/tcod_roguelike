"""Movement action for moving entities."""

from __future__ import annotations

import exceptions
from actions.action_with_direction import ActionWithDirection


class MovementAction(ActionWithDirection):
    """An action that moves an entity in a direction."""

    def perform(self) -> None:
        """Move the entity if the destination is valid."""
        dest_x, dest_y = self.dest_xy
        game_map = self.engine.game_map

        is_blocked = (
            not game_map.in_bounds(dest_x, dest_y)
            or not game_map.tiles['walkable'][dest_x, dest_y]
            or self.blocking_entity is not None
        )
        if is_blocked:
            raise exceptions.ImpossibleActionError('That way is blocked.')

        self.entity.move(self.dx, self.dy)
