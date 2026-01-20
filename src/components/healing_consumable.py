"""Healing consumable that restores HP."""

from __future__ import annotations

from typing import TYPE_CHECKING

import color
import exceptions
from components.consumable import Consumable

if TYPE_CHECKING:
    from actions.item_action import ItemAction


class HealingConsumable(Consumable):
    """A consumable that heals the user."""

    def __init__(self, amount: int) -> None:
        self.amount = amount

    def activate(self, action: ItemAction) -> None:
        """Heal the consumer."""
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)

        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f'You consume the {self.parent.name}, and recover {amount_recovered}.',
                color.health_recovered,
            )
            self.consume()
        else:
            raise exceptions.ImpossibleActionError('Your health is already full.')
