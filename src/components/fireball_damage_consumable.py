import actions
import color
from components.consumable import Consumable
import exceptions
from input_handlers import AreaRangedAttackHandler


class FireballDamageConsumable(Consumable):
    def __init__(self, damage, radius):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer):
        self.engine.message_log.add_message('Select a target location.', color.needs_target)
        return AreaRangedAttackHandler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: actions.ItemAction(
                consumer,
                self.parent,
                xy,
            ),
        )
        return None

    def activate(self, action):
        target_xy = action.target_xy

        if not self.engine.game_map.visible[action.target_xy]:
            raise exceptions.Impossible('You cannot target an area you cannot see.')
        targets_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f'The {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage!'
                )
                actor.fighter.take_damage(self.damage)
                targets_hit = True

        if not targets_hit:
            raise exceptions.Impossible('There are no targets in the radius.')
        self.consume()
