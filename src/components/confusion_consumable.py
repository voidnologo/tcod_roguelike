import actions
import color
import components.ai
import exceptions
from components.consumable import Consumable
from input_handlers import SingleRangedAttackHandler


class ConfusionConsumable(Consumable):
    def __init__(self, number_of_turns):
        self.number_of_turns = number_of_turns

    def get_action(self, consumer):
        self.engine.message_log.add_message('Select a target location.', color.needs_target)
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action):
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
