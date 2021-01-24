import tcod as libtcod

import actions


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


class EventHandler(libtcod.event.EventDispatch[actions.Action]):
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self):
        raise NotImplementedError()

    def ev_quit(self, event):
        raise SystemExit()


class MainGameEventHandler(EventHandler):
    def handle_events(self):
        for event in libtcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action

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
        return action


class GameOverEventHandler(EventHandler):
    def handle_events(self):
        for event in libtcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()

    def ev_keydown(self, event):
        action = None
        key = event.sym
        if key == libtcod.event.K_ESCAPE:
            action = actions.EscapeAction(self.engine.player)
        return action
