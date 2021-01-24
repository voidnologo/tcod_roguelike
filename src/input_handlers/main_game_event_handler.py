import tcod as libtcod

import actions
from input_handlers.base_event_handler import EventHandler
from input_handlers.history_viewer import HistoryViewer
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
            action = actions.EscapeAction(player)
        elif key == libtcod.event.K_v:
            self.engine.event_handler = HistoryViewer(self.engine)
        elif key == libtcod.event.K_g:
            action = actions.PickupAction(player)
        return action
