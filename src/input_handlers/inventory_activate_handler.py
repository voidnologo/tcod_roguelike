"""Event handler for using inventory items."""

from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers.base_event_handler import ActionOrHandler
from input_handlers.inventory_event_handler import InventoryEventHandler

if TYPE_CHECKING:
    from entity.item import Item


class InventoryActivateHandler(InventoryEventHandler):
    """Event handler for using an inventory item."""

    TITLE = 'Select an item to use'

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        """Use the selected item."""
        return item.consumable.get_action(self.engine.player)
