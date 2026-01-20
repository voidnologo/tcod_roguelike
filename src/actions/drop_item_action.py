"""Drop item action for dropping items from inventory."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actions.item_action import ItemAction

if TYPE_CHECKING:
    from entity.actor import Actor
    from entity.item import Item


class DropItemAction(ItemAction):
    """An action that drops an item from the entity's inventory."""

    def __init__(self, entity: Actor, item: Item) -> None:
        super().__init__(entity, item)

    def perform(self) -> None:
        """Drop the item from inventory onto the game map."""
        self.entity.inventory.drop(self.item)
