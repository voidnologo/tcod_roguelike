import actions
import components.inventory
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
