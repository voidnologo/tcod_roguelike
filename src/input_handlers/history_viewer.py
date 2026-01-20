"""Message history viewer event handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.console
import tcod.constants
import tcod.event
from tcod.event import KeySym

from input_handlers import consts
from input_handlers.base_event_handler import ActionOrHandler, EventHandler

if TYPE_CHECKING:
    from engine import Engine


class HistoryViewer(EventHandler):
    """Event handler for viewing message history."""

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the message history panel."""
        super().on_render(console)
        log_console = tcod.console.Console(console.width - 6, console.height - 6)

        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, '┤Message history├', alignment=tcod.constants.CENTER)

        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandler:
        """Handle key presses for navigation."""
        match event.sym:
            case sym if sym in consts.CURSOR_Y_KEYS:
                adjust = consts.CURSOR_Y_KEYS[sym]
                if adjust < 0 and self.cursor == 0:
                    self.cursor = self.log_length - 1
                elif adjust > 0 and self.cursor == self.log_length - 1:
                    self.cursor = 0
                else:
                    self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))
            case KeySym.HOME:
                self.cursor = 0
            case KeySym.END:
                self.cursor = self.log_length - 1
            case _:
                from input_handlers.main_game_event_handler import MainGameEventHandler

                return MainGameEventHandler(self.engine)
        return None
