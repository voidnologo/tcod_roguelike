import tcod as libtcod

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

CONFIRM_KEYS = {
    libtcod.event.K_RETURN,
    libtcod.event.K_KP_ENTER,
}
