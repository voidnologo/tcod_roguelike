"""Event handler for game over state."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod as libtcod

from input_handlers.base_event_handler import ActionOrHandler, EventHandler

if TYPE_CHECKING:
    from tcod.event import KeyDown


class GameOverEventHandler(EventHandler):
    """Event handler for when the player has died."""

    def ev_keydown(self, event: KeyDown) -> ActionOrHandler:
        """Handle key presses. Only escape exits."""
        if event.sym == libtcod.event.K_ESCAPE:
            raise SystemExit()
        return None
