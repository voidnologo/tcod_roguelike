"""Event handler for user prompts."""

from __future__ import annotations

import tcod.event

from input_handlers import consts
from input_handlers.base_event_handler import ActionOrHandler, EventHandler


class AskUserEventHandler(EventHandler):
    """Event handler that prompts the user for input."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandler:
        """Handle key press. By default any non-modifier key exits."""
        if event.sym in consts.MODIFIER_KEYS:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event: tcod.event.MouseButtonDown) -> ActionOrHandler:
        """Handle mouse click. By default any click exits."""
        return self.on_exit()

    def on_exit(self) -> ActionOrHandler:
        """Return to the main game handler."""
        from input_handlers.main_game_event_handler import MainGameEventHandler

        return MainGameEventHandler(self.engine)
