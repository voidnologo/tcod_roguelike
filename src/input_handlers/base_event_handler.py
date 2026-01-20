import tcod as libtcod

import actions
import color
import exceptions


class BaseEventHandler(libtcod.event.EventDispatch):
    def handle_events(self, event):
        """
        Handle an event and return the next active event handler.
        """
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, actions.Action), f'{self!r} can not handle actions.'
        return self

    def on_render(self, console):
        raise NotImplementedError()

    def ev_quit(self, event):
        raise SystemExit()


class EventHandler(BaseEventHandler):
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self, event):
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            # a valid action is performed
            if not self.engine.player.is_alive:
                # the player was killed sometime during or after the action.
                from input_handlers.game_over_event_handler import GameOverEventHandler

                return GameOverEventHandler(self.engine)
            from input_handlers.main_game_event_handler import MainGameEventHandler

            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action):
        """
        Handle actions returned from event methods
        returns True if action will advance a turn
        """
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.ImpossibleActionError as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False  # skip enemy turn on exceptions

        self.engine.handle_enemy_turns()
        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event):
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = (event.tile.x, event.tile.y)

    def on_render(self, console):
        self.engine.render(console)
