"""Confusion consumable that confuses enemies."""

from __future__ import annotations

from typing import TYPE_CHECKING

import actions
import color
import components.ai
import exceptions
from components.consumable import Consumable
from input_handlers import SingleRangedAttackHandler

if TYPE_CHECKING:
    from actions.item_action import ItemAction
    from entity.actor import Actor
    from input_handlers.base_event_handler import ActionOrHandler


class ConfusionConsumable(Consumable):
    """A consumable that confuses the target for a number of turns."""

    def __init__(self, number_of_turns: int) -> None:
        self.number_of_turns = number_of_turns

    def get_action(self, consumer: Actor) -> ActionOrHandler:
        """Prompt the user to select a target."""
        self.engine.message_log.add_message('Select a target location.', color.needs_target)
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: ItemAction) -> None:
        """Confuse the target enemy."""
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise exceptions.ImpossibleActionError('You cannot target an area you cannot see.')
        if not target:
            raise exceptions.ImpossibleActionError('You must select an enemy to target.')
        if target is consumer:
            raise exceptions.ImpossibleActionError('You cannot confuse yourself!')

        self.engine.message_log.add_message(
            f'The eyes of the {target.name} look vacant, as it starts to stumble around!',
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target,
            previous_ai=target.ai,
            turns_remaining=self.number_of_turns,
        )
        self.consume()
