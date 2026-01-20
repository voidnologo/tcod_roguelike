"""Hostile enemy AI that pursues and attacks the player."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actions import MeleeAction, MovementAction, WaitAction
from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from entity.actor import Actor
    from game_types import Position


class HostileEnemy(BaseAI):
    """AI for enemies that actively hunt the player."""

    def __init__(self, entity: Actor) -> None:
        super().__init__(entity)
        self.path: list[Position] = []

    def perform(self) -> None:
        """Chase and attack the player."""
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                MeleeAction(self.entity, dx, dy).perform()
                return
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()
            return
        WaitAction(self.entity).perform()
