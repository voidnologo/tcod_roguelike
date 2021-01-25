import random

from actions import BumpAction
from components.ai.base_ai import BaseAI


class ConfusedEnemy(BaseAI):
    """
    A confused enemy will stumble around aimlessly for a given
    number of turns and then revert to its prior AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(self, entity, previous_ai, turns_remaining):
        super().__init__(entity)
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self):
        # Revert the AI back to original if effect expired
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(f'The {self.entity.name} is no longer confused.')
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )
            self.turns_remaining -= 1
            # The actor will either try to move or attack in the choosen random direction
            # or run into a wall, wasting a turn
            return BumpAction(self.entity, direction_x, direction_y).perform()
