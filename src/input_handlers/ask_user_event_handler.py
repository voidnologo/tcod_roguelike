import tcod as libtcod

from input_handlers.base_event_handler import EventHandler


class AskUserEventHandler(EventHandler):
    def handle_action(self, action):
        if super().handle_action(action):
            from input_handlers.main_game_event_handler import MainGameEventHandler

            self.engine.event_handler = MainGameEventHandler(self.engine)
            return True
        return False

    def ev_keydown(self, event):
        """
        By default any key exits this input handler.
        """
        if event.sym in {  # ignore modifier keys
            libtcod.event.K_LSHIFT,
            libtcod.event.K_RSHIFT,
            libtcod.event.K_LCTRL,
            libtcod.event.K_RCTRL,
            libtcod.event.K_LALT,
            libtcod.event.K_RALT,
        }:
            return None
        return self.on_exit()

    def ev_mousebuttondown(self, event):
        """
        By default any mouse click exits this input handler.
        """
        return self.on_exit()

    def on_exit(self):
        """
        Called when a user is trying to exit or cancel an action.
        By default returns to the main event handler
        """
        from input_handlers.main_game_event_handler import MainGameEventHandler

        self.engine.event_handler = MainGameEventHandler(self.engine)
        return None
