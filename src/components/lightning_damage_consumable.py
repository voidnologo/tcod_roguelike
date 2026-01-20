"""Lightning damage consumable that strikes the nearest enemy."""

from __future__ import annotations

from typing import TYPE_CHECKING

import exceptions
from components.consumable import Consumable

if TYPE_CHECKING:
    from actions.item_action import ItemAction


class LightningDamageConsumable(Consumable):
    """A consumable that strikes the closest visible enemy with lightning."""

    def __init__(self, damage: int, maximum_range: int) -> None:
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action: ItemAction) -> None:
        """Strike the nearest visible enemy with lightning."""
        consumer = action.entity
        target = None
        closest_distance = self.maximum_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f'A lightning bolt strikes the {target.name} with a loud crash, for {self.damage} damage!'
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise exceptions.ImpossibleActionError('No enemy is close enough to strike.')
