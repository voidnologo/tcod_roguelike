"""Main game event handler for normal gameplay."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod as libtcod

import actions
from input_handlers import consts
from input_handlers.base_event_handler import ActionOrHandler, EventHandler
from input_handlers.history_viewer import HistoryViewer
from input_handlers.inventory_activate_handler import InventoryActivateHandler
from input_handlers.inventory_drop_handler import InventoryDropHandler
from input_handlers.look_handler import LookHandler

if TYPE_CHECKING:
    from tcod.event import KeyDown

    from engine import Engine

# Map keys to handler classes
HANDLER_KEYS: dict[int, type[EventHandler]] = {
    libtcod.event.K_v: HistoryViewer,
    libtcod.event.K_i: InventoryActivateHandler,
    libtcod.event.K_d: InventoryDropHandler,
    libtcod.event.K_SLASH: LookHandler,
}


class MainGameEventHandler(EventHandler):
    """Event handler for main gameplay."""

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)

    def ev_keydown(self, event: KeyDown) -> ActionOrHandler:
        """Handle key presses during gameplay."""
        player = self.engine.player
        key = event.sym

        if key == libtcod.event.K_ESCAPE:
            raise SystemExit()

        if key in HANDLER_KEYS:
            return HANDLER_KEYS[key](self.engine)

        if key == libtcod.event.K_g:
            return actions.PickupAction(player)

        if key in consts.MOVE_KEYS:
            dx, dy = consts.MOVE_KEYS[key]
            return actions.BumpAction(player, dx, dy)

        if key in consts.WAIT_KEYS:
            return actions.WaitAction(player)

        return None
