"""Fireball consumable that damages enemies in an area."""

from __future__ import annotations

from typing import TYPE_CHECKING

import actions
import color
import exceptions
from components.consumable import Consumable
from input_handlers import AreaRangedAttackHandler

if TYPE_CHECKING:
    from actions.item_action import ItemAction
    from entity.actor import Actor
    from input_handlers.base_event_handler import ActionOrHandler


class FireballDamageConsumable(Consumable):
    """A consumable that deals fire damage in an area."""

    def __init__(self, damage: int, radius: int) -> None:
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> ActionOrHandler:
        """Prompt the user to select a target area."""
        self.engine.message_log.add_message('Select a target location.', color.needs_target)
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: ItemAction) -> None:
        """Deal fire damage to all actors in the radius."""
        consumer = action.entity
        target_xy = action.target_xy

        if not self.engine.game_map.visible[action.target_xy]:
            raise exceptions.ImpossibleActionError('You cannot target an area you cannot see.')

        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor is consumer:
                continue
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f'The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!'
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise exceptions.ImpossibleActionError('There are no targets in the radius.')
        self.consume()
