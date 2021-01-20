import tcod as libtcod


def handle_keys(key):
    mapping = {
        libtcod.event.K_j: {'move': (0, 1)},  # down
        libtcod.event.K_k: {'move': (0, -1)},  # up
        libtcod.event.K_h: {'move': (-1, 0)},  # left
        libtcod.event.K_l: {'move': (1, 0)},  # right
    }
    return mapping.get(key.sym, {})
