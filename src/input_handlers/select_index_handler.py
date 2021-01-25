import tcod as libtcod

import color
from input_handlers import consts
from input_handlers.ask_user_event_handler import AskUserEventHandler


class SelectIndexHandler(AskUserEventHandler):
    """
    Handles asking the user for an index on the map.
    """

    def __init__(self, engine):
        super().__init__(engine)
        player = self.engine.player
        engine.mouse_location = (player.x, player.y)

    def on_render(self, console):
        """
        Highlight the tile under the cursor.
        """
        super().on_render(console)
        x, y = self.engine.mouse_location
        console.tiles_rgb['bg'][x, y] = color.white
        console.tiles_rgb['fg'][x, y] = color.black

    def ev_keydown(self, event):
        key = event.sym
        if key in consts.MOVE_KEYS:
            modifier = 1  # Holding modifier keys will speed up key movement
            if event.mod & (libtcod.event.KMOD_LSHIFT | libtcod.event.KMOD_RSHIFT):
                modifier *= 5
            if event.mod & (libtcod.event.KMOD_LCTRL | libtcod.event.KMOD_RCTRL):
                modifier *= 10
            if event.mod & (libtcod.event.KMOD_LALT | libtcod.event.KMOD_RALT):
                modifier *= 20

            x, y = self.engine.mouse_location
            dx, dy = consts.MOVE_KEYS[key]
            x += dx * modifier
            y += dy * modifier
            # Restrict the cursor inddex to the map size.
            x = max(0, min(x, self.engine.game_map.width - 1))
            y = max(0, min(y, self.engine.game_map.height - 1))
            self.engine.mouse_location = (x, y)
            return None
        elif key in consts.CONFIRM_KEYS:
            return self.on_index_selected(*self.engine.mouse_location)
        return super().ev_keydown(event)

    def ev_mousebuttondown(self, event):
        """
        Left click confirms a selection
        """
        if self.engine.game_map.in_bounds(*event.tile):
            if event.button == 1:
                return self.on_index_selected(*event.tile)
        return super().ev_mousebuttondown(event)

    def on_index_selected(self, x, y):
        raise NotImplementedError()
