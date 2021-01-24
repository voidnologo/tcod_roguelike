from input_handlers.inventory_event_handler import InventoryEventHandler


class InventoryActivateHandler(InventoryEventHandler):
    """
    Handle using an inventory item
    """

    TITLE = 'Select an item to use'

    def on_item_selected(self, item):
        return item.consumable.get_action(self.engine.player)
