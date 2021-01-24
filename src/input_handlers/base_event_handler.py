import tcod as libtcod

import actions
import color
import exceptions


class EventHandler(libtcod.event.EventDispatch[actions.Action]):
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self, event):
        self.handle_actions(self.dispatch(event))

    def handle_actions(self, action):
        """
        Handle actions returned from event methods
        returns True if action will advance a turn
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.Impossible as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # skip enemy turn on exceptions

        self.engine.handle_enemy_turns()
        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event):
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = (event.tile.x, event.tile.y)

    def ev_quit(self, event):
        raise SystemExit()

    def on_render(self, console):
        self.engine.render(console)
