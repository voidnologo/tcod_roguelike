import tcod as libtcod

import actions


class EventHandler(libtcod.event.EventDispatch[actions.Action]):
    def ev_quit(self, event):
        raise SystemExit()

    def ev_keydown(self, event):
        mapping = {
            libtcod.event.K_j: actions.BumpAction(dx=0, dy=1),  # down
            libtcod.event.K_k: actions.BumpAction(dx=0, dy=-1),  # up
            libtcod.event.K_h: actions.BumpAction(dx=-1, dy=0),  # left
            libtcod.event.K_l: actions.BumpAction(dx=1, dy=0),  # right
            libtcod.event.K_ESCAPE: actions.EscapeAction,
        }
        return mapping.get(event.sym, None)
