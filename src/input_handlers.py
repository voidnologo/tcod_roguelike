import tcod as libtcod

import actions
import color
import exceptions


MOVE_KEYS = {
    # Arrow keys.
    libtcod.event.K_UP: (0, -1),
    libtcod.event.K_DOWN: (0, 1),
    libtcod.event.K_LEFT: (-1, 0),
    libtcod.event.K_RIGHT: (1, 0),
    libtcod.event.K_HOME: (-1, -1),
    libtcod.event.K_END: (-1, 1),
    libtcod.event.K_PAGEUP: (1, -1),
    libtcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    libtcod.event.K_KP_1: (-1, 1),
    libtcod.event.K_KP_2: (0, 1),
    libtcod.event.K_KP_3: (1, 1),
    libtcod.event.K_KP_4: (-1, 0),
    libtcod.event.K_KP_6: (1, 0),
    libtcod.event.K_KP_7: (-1, -1),
    libtcod.event.K_KP_8: (0, -1),
    libtcod.event.K_KP_9: (1, -1),
    # Vi keys.
    libtcod.event.K_h: (-1, 0),
    libtcod.event.K_j: (0, 1),
    libtcod.event.K_k: (0, -1),
    libtcod.event.K_l: (1, 0),
    libtcod.event.K_y: (-1, -1),
    libtcod.event.K_u: (1, -1),
    libtcod.event.K_b: (-1, 1),
    libtcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    libtcod.event.K_PERIOD,
    libtcod.event.K_KP_5,
    libtcod.event.K_CLEAR,
}

CURSOR_Y_KEYS = {
    libtcod.event.K_UP: -1,
    libtcod.event.K_DOWN: 1,
    libtcod.event.K_PAGEUP: -10,
    libtcod.event.K_PAGEDOWN: 10,
}


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


class MainGameEventHandler(EventHandler):
    def ev_keydown(self, event):
        action = None
        player = self.engine.player
        key = event.sym
        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = actions.BumpAction(player, dx, dy)
        elif key in WAIT_KEYS:
            action = actions.WaitAction(player)
        elif key == libtcod.event.K_ESCAPE:
            action = actions.EscapeAction(player)
        elif key == libtcod.event.K_v:
            self.engine.event_handler = HistoryViewer(self.engine)
        elif key == libtcod.event.K_g:
            action = actions.PickupAction(player)
        return action


class GameOverEventHandler(EventHandler):
    def ev_keydown(self, event):
        if event.sym == libtcod.event.K_ESCAPE:
            raise SystemExit()
            # action = actions.EscapeAction(self.engine.player)
        # return action


class HistoryViewer(EventHandler):
    ''' Print message history in a larger window which can be navigated '''

    def __init__(self, engine):
        super().__init__(engine)
        self.log_length = len(engine.message_log.messages)
        self.cursor = self.log_length - 1

    def on_render(self, console):
        super().on_render(console)  # draw game as background
        log_console = libtcod.Console(console.width - 6, console.height - 6)

        # Draw a frame with a custom banner title
        log_console.draw_frame(0, 0, log_console.width, log_console.height)
        log_console.print_box(0, 0, log_console.width, 1, '┤Message history├', alignment=libtcod.CENTER)

        # Render the message log using the cursor parameter
        self.engine.message_log.render_messages(
            log_console,
            1,
            1,
            log_console.width - 2,
            log_console.height - 2,
            self.engine.message_log.messages[: self.cursor + 1],
        )
        log_console.blit(console, 3, 3)

    def ev_keydown(self, event):
        # fancy conditional movement to make it feel good
        if event.sym in CURSOR_Y_KEYS:
            adjust = CURSOR_Y_KEYS[event.sym]
            if adjust < 0 and self.cursor == 0:
                # only move from the top to the bottom when youre on the edge
                self.cursor = self.log_length - 1
            elif adjust > 0 and self.cursor == self.log_length - 1:
                # same with bottom to top movement
                self.cursor = 0
            else:
                # otherwise move while staying clamped to the bounds of the history log
                self.cursor = max(0, min(self.cursor + adjust, self.log_length - 1))

        elif event.sym == libtcod.event.K_HOME:
            self.cursor = 0  # move directly to the top message
        elif event.sym == libtcod.event.K_END:
            self.cursor == self.log_length - 1  # move directly to last message
        else:  # any other key moves back to main game state
            self.engine.event_handler = MainGameEventHandler(self.engine)
