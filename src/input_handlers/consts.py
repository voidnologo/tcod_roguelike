"""Constants for input handling."""

from __future__ import annotations

from tcod.event import KeySym

from game_types import Direction

MOVE_KEYS: dict[KeySym, Direction] = {
    # Arrow keys
    KeySym.UP: (0, -1),
    KeySym.DOWN: (0, 1),
    KeySym.LEFT: (-1, 0),
    KeySym.RIGHT: (1, 0),
    KeySym.HOME: (-1, -1),
    KeySym.END: (-1, 1),
    KeySym.PAGEUP: (1, -1),
    KeySym.PAGEDOWN: (1, 1),
    # Numpad keys
    KeySym.KP_1: (-1, 1),
    KeySym.KP_2: (0, 1),
    KeySym.KP_3: (1, 1),
    KeySym.KP_4: (-1, 0),
    KeySym.KP_6: (1, 0),
    KeySym.KP_7: (-1, -1),
    KeySym.KP_8: (0, -1),
    KeySym.KP_9: (1, -1),
    # Vi keys
    KeySym.h: (-1, 0),
    KeySym.j: (0, 1),
    KeySym.k: (0, -1),
    KeySym.l: (1, 0),
    KeySym.y: (-1, -1),
    KeySym.u: (1, -1),
    KeySym.b: (-1, 1),
    KeySym.n: (1, 1),
}

WAIT_KEYS: set[KeySym] = {
    KeySym.PERIOD,
    KeySym.KP_5,
    KeySym.CLEAR,
}

CURSOR_Y_KEYS: dict[KeySym, int] = {
    KeySym.UP: -1,
    KeySym.DOWN: 1,
    KeySym.PAGEUP: -10,
    KeySym.PAGEDOWN: 10,
}

CONFIRM_KEYS: set[KeySym] = {
    KeySym.RETURN,
    KeySym.KP_ENTER,
}

MODIFIER_KEYS: set[KeySym] = {
    KeySym.LSHIFT,
    KeySym.RSHIFT,
    KeySym.LCTRL,
    KeySym.RCTRL,
    KeySym.LALT,
    KeySym.RALT,
}
