"""Event handler for user prompts."""

from __future__ import annotations

from typing import TYPE_CHECKING

from input_handlers import consts
from input_handlers.base_event_handler import ActionOrHandler, EventHandler

if TYPE_CHECKING:
    from tcod.event import KeyDown, MouseButtonDown


class AskUserEventHandler(EventHandler):
    """Event handler that prompts the user for input."""

    def ev_keydown(self, event: KeyDown) -> ActionOrHandler:
        """Handle key press. By default any non-modifier key exits."""
        if event.sym in consts.MODIFIER_KEYS:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: MouseButtonDown) -> ActionOrHandler:
        """Handle mouse click. By default any click exits."""
        return self.on_exit()

    def on_exit(self) -> ActionOrHandler:
        """Return to the main game handler."""
        from input_handlers.main_game_event_handler import MainGameEventHandler

        return MainGameEventHandler(self.engine)
