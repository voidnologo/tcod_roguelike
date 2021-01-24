import actions
import color
import components.inventory
import exceptions
from components.base_component import BaseComponent


class Consumable(BaseComponent):
    parent = None

    def get_action(self, consumer):
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action):
        """
        Invoke this items ability
        `action` is the context for this activation
        """
        raise NotImplementedError()

    def consume(self):
        """
        Remove consumed item from containing inventory
        """
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


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
            raise exceptions.Impossible('Your health is already full.')
