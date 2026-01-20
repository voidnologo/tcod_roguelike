"""Bump action that decides between melee and movement."""

from __future__ import annotations

from actions.action_with_direction import ActionWithDirection
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction


class BumpAction(ActionWithDirection):
    """An action that attacks if there's a target, otherwise moves."""

    def perform(self) -> None:
        """Attack target actor or move to destination."""
        if self.target_actor:
            MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            MovementAction(self.entity, self.dx, self.dy).perform()
