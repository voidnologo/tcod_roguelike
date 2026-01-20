import exceptions
from components.consumable import Consumable


class LighteningDamageConsumable(Consumable):
    def __init__(self, damage, maximum_range):
        self.damage = damage
        self.maximum_range = maximum_range

    def activate(self, action):
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
                f'A lightening bolt strike the {target.name} with a loud crash, for {self.damage} damage!'
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise exceptions.ImpossibleActionError('No enemy is close enough to strike.')
