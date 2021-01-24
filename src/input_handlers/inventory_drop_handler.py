import actions
from input_handlers.inventory_event_handler import InventoryEventHandler


class InventoryDropHandler(InventoryEventHandler):
    """
    Handle dropping an inventory item
    """

    TITLE = 'Select an item to drop'

    def on_item_selected(self, item):
        return actions.DropItemAction(self.engine.player, item)
