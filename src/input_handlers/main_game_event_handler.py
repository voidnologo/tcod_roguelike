import tcod as libtcod

import actions
from input_handlers import consts
from input_handlers.base_event_handler import EventHandler
from input_handlers.history_viewer import HistoryViewer
from input_handlers.inventory_activate_handler import InventoryActivateHandler
from input_handlers.inventory_drop_handler import InventoryDropHandler
from input_handlers.look_handler import LookHandler


class MainGameEventHandler(EventHandler):
    def _get_handler_for_key(self, key):
        """Return a new handler for keys that switch game state, or None."""
        handler_map = {
            libtcod.event.K_v: HistoryViewer,
            libtcod.event.K_i: InventoryActivateHandler,
            libtcod.event.K_d: InventoryDropHandler,
            libtcod.event.K_SLASH: LookHandler,
        }
        handler_class = handler_map.get(key)
        return handler_class(self.engine) if handler_class else None

    def ev_keydown(self, event):
        player = self.engine.player
        key = event.sym

        if key == libtcod.event.K_ESCAPE:
            raise SystemExit()

        handler = self._get_handler_for_key(key)
        if handler:
            return handler

        if key in consts.MOVE_KEYS:
            dx, dy = consts.MOVE_KEYS[key]
            return actions.BumpAction(player, dx, dy)
        if key in consts.WAIT_KEYS:
            return actions.WaitAction(player)
        if key == libtcod.event.K_g:
            return actions.PickupAction(player)

        return None
