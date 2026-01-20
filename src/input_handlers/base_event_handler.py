"""Base event handler classes."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod as libtcod

import actions
import color
import exceptions

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.event import Event, MouseMotion, Quit

    from actions.base_action import Action
    from engine import Engine

type ActionOrHandler = Action | BaseEventHandler | None


class BaseEventHandler(libtcod.event.EventDispatch[ActionOrHandler]):
    """Base class for event handlers."""

    def handle_events(self, event: Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        state = self.dispatch(event)
        if isinstance(state, BaseEventHandler):
            return state
        assert not isinstance(state, actions.Action), f'{self!r} can not handle actions.'
        return self

    def on_render(self, console: Console) -> None:
        """Render the handler's state to the console."""
        raise NotImplementedError()

    def ev_quit(self, event: Quit) -> ActionOrHandler:
        """Handle quit event."""
        raise SystemExit()


class EventHandler(BaseEventHandler):
    """Event handler that has access to the game engine."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def handle_events(self, event: Event) -> BaseEventHandler:
        """Handle an event and return the next active event handler."""
        action_or_state = self.dispatch(event)
        if isinstance(action_or_state, BaseEventHandler):
            return action_or_state
        if self.handle_action(action_or_state):
            if not self.engine.player.is_alive:
                from input_handlers.game_over_event_handler import GameOverEventHandler

                return GameOverEventHandler(self.engine)
            from input_handlers.main_game_event_handler import MainGameEventHandler

            return MainGameEventHandler(self.engine)
        return self

    def handle_action(self, action: Action | None) -> bool:
        """Handle actions returned from event methods. Returns True if action advances turn."""
        if action is None:
            return False

        try:
            action.perform()
        except exceptions.ImpossibleActionError as exc:
            self.engine.message_log.add_message(exc.args[0], color.impossible)
            return False

        self.engine.handle_enemy_turns()
        self.engine.update_fov()
        return True

    def ev_mousemotion(self, event: MouseMotion) -> ActionOrHandler:
        """Handle mouse motion."""
        if self.engine.game_map.in_bounds(event.tile.x, event.tile.y):
            self.engine.mouse_location = (event.tile.x, event.tile.y)
        return None

    def on_render(self, console: Console) -> None:
        """Render the game state."""
        self.engine.render(console)
