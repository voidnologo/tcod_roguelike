"""Event handler for dropping inventory items."""

from __future__ import annotations

from typing import TYPE_CHECKING

import actions
from input_handlers.base_event_handler import ActionOrHandler
from input_handlers.inventory_event_handler import InventoryEventHandler

if TYPE_CHECKING:
    from entity.item import Item


class InventoryDropHandler(InventoryEventHandler):
    """Event handler for dropping an inventory item."""

    TITLE = 'Select an item to drop'

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        """Drop the selected item."""
        return actions.DropItemAction(self.engine.player, item)
