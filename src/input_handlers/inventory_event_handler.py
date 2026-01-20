"""Event handler for inventory management."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod as libtcod

import color
from input_handlers.ask_user_event_handler import AskUserEventHandler
from input_handlers.base_event_handler import ActionOrHandler

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.event import KeyDown

    from entity.item import Item


class InventoryEventHandler(AskUserEventHandler):
    """Event handler for inventory item selection."""

    TITLE = '<missing title>'

    def on_render(self, console: Console) -> None:
        """Render the inventory menu."""
        super().on_render(console)
        number_of_items = len(self.engine.player.inventory.items)

        height = max(3, number_of_items + 2)
        x = 40 if self.engine.player.x <= 30 else 0
        y = 0
        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord('a') + i)
                console.print(x + 1, y + i + 1, f'({item_key}) {item.name})')
        else:
            console.print(x + 1, y + 1, '(Empty)')

    def ev_keydown(self, event: KeyDown) -> ActionOrHandler:
        """Handle key presses for item selection."""
        player = self.engine.player
        key = event.sym
        index = key - libtcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message('Invalid entry.', color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item: Item) -> ActionOrHandler:
        """Called when an item is selected. Must be overridden."""
        raise NotImplementedError()
