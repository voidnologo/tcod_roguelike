"""Base consumable component for usable items."""

from __future__ import annotations

from typing import TYPE_CHECKING

import actions
import components.inventory
from components.base_component import BaseComponent

if TYPE_CHECKING:
    from actions.item_action import ItemAction
    from entity.actor import Actor
    from entity.item import Item
    from input_handlers.base_event_handler import ActionOrHandler


class Consumable(BaseComponent):
    """Base class for consumable item components."""

    parent: Item

    def get_action(self, consumer: Actor) -> ActionOrHandler:
        """Return the action for using this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: ItemAction) -> None:
        """Invoke this item's ability. Must be overridden by subclasses."""
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from the containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)
