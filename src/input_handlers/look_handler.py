"""Event handler for look mode."""

from __future__ import annotations

from input_handlers.base_event_handler import ActionOrHandler
from input_handlers.select_index_handler import SelectIndexHandler


class LookHandler(SelectIndexHandler):
    """Event handler that lets the player look around with the keyboard."""

    def on_index_selected(self, x: int, y: int) -> ActionOrHandler:
        """Return to main game when a position is selected."""
        from input_handlers.main_game_event_handler import MainGameEventHandler

        return MainGameEventHandler(self.engine)
