"""Event handler for selecting map positions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import tcod as libtcod

import color
from input_handlers import consts
from input_handlers.ask_user_event_handler import AskUserEventHandler
from input_handlers.base_event_handler import ActionOrHandler

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.event import KeyDown, MouseButtonDown

    from engine import Engine


def get_movement_modifier(mod: int) -> int:
    """Calculate movement speed modifier based on held keys."""
    modifier = 1
    if mod & (libtcod.event.KMOD_LSHIFT | libtcod.event.KMOD_RSHIFT):
        modifier *= 5
    if mod & (libtcod.event.KMOD_LCTRL | libtcod.event.KMOD_RCTRL):
        modifier *= 10
    if mod & (libtcod.event.KMOD_LALT | libtcod.event.KMOD_RALT):
        modifier *= 20
    return modifier


class SelectIndexHandler(AskUserEventHandler):
    """Event handler for selecting a position on the map."""

    def __init__(self, engine: Engine) -> None:
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = (player.x, player.y)

    def on_render(self, console: Console) -> None:
        """Highlight the tile under the cursor."""
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb['bg'][x, y] = color.white
        console.tiles_rgb['fg'][x, y] = color.black

    def ev_keydown(self, event: KeyDown) -> ActionOrHandler:
        """Handle key presses for cursor movement."""
        key = event.sym
        if key in consts.MOVE_KEYS:
            modifier = get_movement_modifier(event.mod)

            x, y = self.engine.mouse_location
            dx, dy = consts.MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = (x, y)
            return None
        elif key in consts.CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event: MouseButtonDown) -> ActionOrHandler:
        """Handle mouse clicks for selection."""
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x: int, y: int) -> ActionOrHandler:
        """Called when a position is selected. Must be overridden."""
        raise NotImplementedError()
