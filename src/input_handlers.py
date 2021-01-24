import tcod as libtcod

import actions


class EventHandler(libtcod.event.EventDispatch[actions.Action]):
    def __init__(self, engine):
        self.engine = engine

    def handle_events(self):
        for event in libtcod.event.wait():
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action

    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        player = self.engine.player
        mapping = {
            libtcod.event.K_j: actions.BumpAction(player, dx=0, dy=1),  # down
            libtcod.event.K_k: actions.BumpAction(player, dx=0, dy=-1),  # up
            libtcod.event.K_h: actions.BumpAction(player, dx=-1, dy=0),  # left
            libtcod.event.K_l: actions.BumpAction(player, dx=1, dy=0),  # right
            libtcod.event.K_ESCAPE: actions.EscapeAction(player),
        }
        return mapping.get(event.sym, None)
