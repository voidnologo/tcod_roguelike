"""Melee action for attacking adjacent entities."""

from __future__ import annotations

import color
import exceptions
from actions.action_with_direction import ActionWithDirection


class MeleeAction(ActionWithDirection):
    """An action that attacks an adjacent target."""

    def perform(self) -> None:
        """Attack the target actor at the destination."""
        target = self.target_actor
        if not target:
            raise exceptions.ImpossibleActionError('Nothing to attack.')

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f'{self.entity.name.capitalize()} attacks {target.name}'
        attack_color = color.player_atk if self.entity is self.engine.player else color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f'{attack_desc} for {damage} hit points.', attack_color)
            target.fighter.take_damage(damage)
        else:
            self.engine.message_log.add_message(f'{attack_desc} does no damage.', attack_color)
