import tcod as libtcod

from input_handlers.base_event_handler import EventHandler
from input_handlers import consts


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
        if event.sym in consts.CURSOR_Y_KEYS:
            adjust = consts.CURSOR_Y_KEYS[event.sym]
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
            from input_handlers.main_game_event_handler import MainGameEventHandler

            return MainGameEventHandler(self.engine)
        return None
