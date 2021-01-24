import tcod as libtcod

from input_handlers.base_event_handler import EventHandler


class GameOverEventHandler(EventHandler):
    def ev_keydown(self, event):
        if event.sym == libtcod.event.K_ESCAPE:
            raise SystemExit()
