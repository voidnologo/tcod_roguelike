"""Main game event handler for normal gameplay."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod.event
from tcod.event import KeySym

import actions
from input_handlers import consts
from input_handlers.base_event_handler import ActionOrHandler, EventHandler
from input_handlers.history_viewer import HistoryViewer
from input_handlers.inventory_activate_handler import InventoryActivateHandler
from input_handlers.inventory_drop_handler import InventoryDropHandler
from input_handlers.look_handler import LookHandler

if TYPE_CHECKING:
    from engine import Engine

# Map keys to handler classes
HANDLER_KEYS: dict[KeySym, type[EventHandler]] = {
    KeySym.v: HistoryViewer,
    KeySym.i: InventoryActivateHandler,
    KeySym.d: InventoryDropHandler,
    KeySym.SLASH: LookHandler,
}


class MainGameEventHandler(EventHandler):
    """Event handler for main gameplay."""

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

    def ev_keydown(self, event: tcod.event.KeyDown) -> ActionOrHandler:
        """Handle key presses during gameplay."""
        player = self.engine.player
        key = event.sym

        if key == KeySym.ESCAPE:
            raise SystemExit()

        if key in HANDLER_KEYS:
            return HANDLER_KEYS[key](self.engine)

        if key == KeySym.g:
            return actions.PickupAction(player)

        if key in consts.MOVE_KEYS:
            dx, dy = consts.MOVE_KEYS[key]
            return actions.BumpAction(player, dx, dy)

        if key in consts.WAIT_KEYS:
            return actions.WaitAction(player)

        return None
