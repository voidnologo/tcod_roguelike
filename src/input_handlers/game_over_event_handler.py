"""Event handler for game over state."""

from __future__ import annotations

import tcod.event
from tcod.event import KeySym

from input_handlers.base_event_handler import ActionOrHandler, EventHandler


class GameOverEventHandler(EventHandler):
    """Event handler for when the player has died."""

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandler:
        """Handle key presses. Only escape exits."""
        if event.sym == KeySym.ESCAPE:
            raise SystemExit()
        return None
