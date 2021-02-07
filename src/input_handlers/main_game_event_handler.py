import tcod as libtcod

import actions
from input_handlers.base_event_handler import EventHandler
from input_handlers.history_viewer import HistoryViewer
from input_handlers.inventory_activate_handler import InventoryActivateHandler
from input_handlers.inventory_drop_handler import InventoryDropHandler
from input_handlers.look_handler import LookHandler
from input_handlers import consts


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event):
        action = None
        player = self.engine.player
        key = event.sym
        if key in consts.MOVE_KEYS:
            dx, dy = consts.MOVE_KEYS[key]
            action = actions.BumpAction(player, dx, dy)
        elif key in consts.WAIT_KEYS:
            action = actions.WaitAction(player)
        elif key == libtcod.event.K_ESCAPE:
            raise SystemExit()
        elif key == libtcod.event.K_v:
            return HistoryViewer(self.engine)
        elif key == libtcod.event.K_g:
            action = actions.PickupAction(player)
        elif key == libtcod.event.K_i:
            return InventoryActivateHandler(self.engine)
        elif key == libtcod.event.K_d:
            return InventoryDropHandler(self.engine)
        elif key == libtcod.event.K_SLASH:
            return LookHandler(self.engine)
        return action
