import color
import exceptions
from components.consumable import Consumable


class HealingConsumable(Consumable):
    def __init__(self, amount):
        self.amount = amount

    def activate(self, action):
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
