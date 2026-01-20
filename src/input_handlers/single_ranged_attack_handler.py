"""Event handler for single target ranged attacks."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from input_handlers.base_event_handler import ActionOrHandler
from input_handlers.select_index_handler import SelectIndexHandler

if TYPE_CHECKING:
    from engine import Engine
    from game_types import Position


class SingleRangedAttackHandler(SelectIndexHandler):
    """Event handler for selecting a single target for an attack."""

    def __init__(
        self,
        engine: Engine,
        callback: Callable[[Position], ActionOrHandler],
    ) -> None:
        super().__init__(engine)
        self.callback = callback

    def on_index_selected(self, x: int, y: int) -> ActionOrHandler:
        """Execute the callback with the selected position."""
        return self.callback((x, y))
