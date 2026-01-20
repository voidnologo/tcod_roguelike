"""Inventory component for storing items."""

from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.actor import Actor
    from entity.item import Item


class Inventory(BaseComponent):
    """Component for entities that can hold items."""

    parent: Actor

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.items: list[Item] = []

    def drop(self, item: Item) -> None:
        """Remove an item from the inventory and place it on the game map."""
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)
        self.engine.message_log.add_message(f'You dropped the {item.name}.')

    @property
    def full(self) -> bool:
        """Return True if the inventory is at capacity."""
        return len(self.items) >= self.capacity
