"""Event handler for area ranged attacks."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

import tcod.console

import color
from input_handlers.base_event_handler import ActionOrHandler
from input_handlers.select_index_handler import SelectIndexHandler

if TYPE_CHECKING:
    from engine import Engine
    from game_types import Position


class AreaRangedAttackHandler(SelectIndexHandler):
    """Event handler for selecting an area target for an attack."""

    def __init__(
        self,
        engine: Engine,
        radius: int,
        callback: Callable[[Position], ActionOrHandler],
    ) -> None:
        super().__init__(engine)
        self.radius = radius
        self.callback = callback

    def on_render(self, console: tcod.console.Console) -> None:
        """Render the targeting area."""
        super().on_render(console)
        x, y = self.engine.mouse_location

        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius * 2 + 3,
            height=self.radius * 2 + 3,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x: int, y: int) -> ActionOrHandler:
        """Execute the callback with the selected position."""
        return self.callback((x, y))
