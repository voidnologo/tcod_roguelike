"""Confused enemy AI that moves randomly."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

from actions import BumpAction
from components.ai.base_ai import BaseAI

if TYPE_CHECKING:
    from entity.actor import Actor


# All eight directions for random movement
DIRECTIONS = [
    (-1, -1),  # Northwest
    (0, -1),   # North
    (1, -1),   # Northeast
    (-1, 0),   # West
    (1, 0),    # East
    (-1, 1),   # Southwest
    (0, 1),    # South
    (1, 1),    # Southeast
]


class ConfusedEnemy(BaseAI):
    """AI for confused enemies that stumble randomly."""

    def __init__(
        self,
        entity: Actor,
        previous_ai: BaseAI | None,
        turns_remaining: int,
    ) -> None:
        super().__init__(entity)
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        """Move randomly or revert to previous AI when confusion ends."""
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(f'The {self.entity.name} is no longer confused.')
            self.entity.ai = self.previous_ai
            if self.previous_ai:
                self.previous_ai.perform()
        else:
            direction_x, direction_y = random.choice(DIRECTIONS)
            self.turns_remaining -= 1
            BumpAction(self.entity, direction_x, direction_y).perform()
