import color
import exceptions
from actions.action_with_direction import ActionWithDirection


class MeleeAction(ActionWithDirection):
    def perform(self):
        target = self.target_actor
        if not target:
            raise exceptions.ImpossibleActionError('Nothing to attack.')

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f'{self.entity.name.capitalize()} attacks {target.name}'
        attack_color = color.player_atk if self.entity is self.engine.player else color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f'{attack_desc} for {damage} hit points.', attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f'{attack_desc} does no damage.', attack_color)
