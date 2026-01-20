"""Color definitions for the roguelike game.

All colors are defined as module-level constants and can also be accessed
via the Colors class for IDE autocompletion (e.g., Colors.WHITE, Colors.HEALTHY).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_types import ColorRGB

# =============================================================================
# Basic Colors
# =============================================================================
WHITE: ColorRGB = (0xFF, 0xFF, 0xFF)
BLACK: ColorRGB = (0x00, 0x00, 0x00)
RED: ColorRGB = (0xFF, 0x00, 0x00)
GREEN: ColorRGB = (0x00, 0xFF, 0x00)
BLUE: ColorRGB = (0x00, 0x00, 0xFF)
YELLOW: ColorRGB = (0xFF, 0xFF, 0x00)
CYAN: ColorRGB = (0x3F, 0xFF, 0xFF)
MAGENTA: ColorRGB = (0xFF, 0x00, 0xFF)
ORANGE: ColorRGB = (0xFF, 0xA5, 0x00)
PURPLE: ColorRGB = (0x80, 0x00, 0x80)

# Grays
LIGHT_GRAY: ColorRGB = (0xC0, 0xC0, 0xC0)
GRAY: ColorRGB = (0x80, 0x80, 0x80)
DARK_GRAY: ColorRGB = (0x40, 0x40, 0x40)

# =============================================================================
# Semantic/Status Colors
# =============================================================================
# Health states
HEALTHY: ColorRGB = (0x00, 0xFF, 0x00)
WOUNDED: ColorRGB = (0xFF, 0xFF, 0x00)
CRITICAL: ColorRGB = (0xFF, 0x00, 0x00)

# Combat
PLAYER_ATTACK: ColorRGB = (0xE0, 0xE0, 0xE0)
ENEMY_ATTACK: ColorRGB = (0xFF, 0xC0, 0xC0)
DAMAGE: ColorRGB = (0xFF, 0x40, 0x40)

# Status effects
EFFECT_APPLIED: ColorRGB = (0x3F, 0xFF, 0x3F)
EFFECT_EXPIRED: ColorRGB = (0x80, 0x80, 0x80)
CONFUSED: ColorRGB = (0xCF, 0x3F, 0xFF)
POISONED: ColorRGB = (0x00, 0xFF, 0x00)

# UI feedback
INVALID_ACTION: ColorRGB = (0xFF, 0xFF, 0x00)
IMPOSSIBLE_ACTION: ColorRGB = (0x80, 0x80, 0x80)
ERROR: ColorRGB = (0xFF, 0x40, 0x40)
SUCCESS: ColorRGB = (0x00, 0xFF, 0x00)
INFO: ColorRGB = (0x20, 0xA0, 0xFF)
WARNING: ColorRGB = (0xFF, 0xFF, 0x00)

# Targeting
NEEDS_TARGET: ColorRGB = (0x3F, 0xFF, 0xFF)
TARGET_VALID: ColorRGB = (0x00, 0xFF, 0x00)
TARGET_INVALID: ColorRGB = (0xFF, 0x00, 0x00)

# =============================================================================
# Death/Corpse Colors
# =============================================================================
PLAYER_DEATH: ColorRGB = (0xFF, 0x30, 0x30)
ENEMY_DEATH: ColorRGB = (0xFF, 0xA0, 0x30)
CORPSE: ColorRGB = (0xBF, 0x00, 0x00)

# =============================================================================
# UI Element Colors
# =============================================================================
# Health bar
BAR_TEXT: ColorRGB = WHITE
BAR_FILLED: ColorRGB = (0x00, 0x60, 0x00)
BAR_EMPTY: ColorRGB = (0x40, 0x10, 0x10)

# Menu
MENU_TITLE: ColorRGB = (0xFF, 0xFF, 0x3F)
MENU_TEXT: ColorRGB = WHITE
MENU_HIGHLIGHT: ColorRGB = (0xFF, 0xFF, 0x00)

# Messages
WELCOME_TEXT: ColorRGB = (0x20, 0xA0, 0xFF)

# =============================================================================
# Legacy aliases (for backwards compatibility)
# =============================================================================
white = WHITE
black = BLACK
red = RED

player_atk = PLAYER_ATTACK
enemy_atk = ENEMY_ATTACK
needs_target = NEEDS_TARGET
status_effect_applied = EFFECT_APPLIED

player_die = PLAYER_DEATH
enemy_die = ENEMY_DEATH

welcome_text = WELCOME_TEXT

bar_text = BAR_TEXT
bar_filled = BAR_FILLED
bar_empty = BAR_EMPTY

invalid = INVALID_ACTION
impossible = IMPOSSIBLE_ACTION
error = ERROR

health_recovered = HEALTHY

menu_title = MENU_TITLE
menu_text = MENU_TEXT


class Colors:
    """Class providing access to all colors with IDE autocompletion.

    Usage:
        from color import Colors
        my_color = Colors.WHITE
        status = Colors.HEALTHY
    """

    # Basic colors
    WHITE = WHITE
    BLACK = BLACK
    RED = RED
    GREEN = GREEN
    BLUE = BLUE
    YELLOW = YELLOW
    CYAN = CYAN
    MAGENTA = MAGENTA
    ORANGE = ORANGE
    PURPLE = PURPLE

    # Grays
    LIGHT_GRAY = LIGHT_GRAY
    GRAY = GRAY
    DARK_GRAY = DARK_GRAY

    # Health states
    HEALTHY = HEALTHY
    WOUNDED = WOUNDED
    CRITICAL = CRITICAL

    # Combat
    PLAYER_ATTACK = PLAYER_ATTACK
    ENEMY_ATTACK = ENEMY_ATTACK
    DAMAGE = DAMAGE

    # Status effects
    EFFECT_APPLIED = EFFECT_APPLIED
    EFFECT_EXPIRED = EFFECT_EXPIRED
    CONFUSED = CONFUSED
    POISONED = POISONED

    # UI feedback
    INVALID_ACTION = INVALID_ACTION
    IMPOSSIBLE_ACTION = IMPOSSIBLE_ACTION
    ERROR = ERROR
    SUCCESS = SUCCESS
    INFO = INFO
    WARNING = WARNING

    # Targeting
    NEEDS_TARGET = NEEDS_TARGET
    TARGET_VALID = TARGET_VALID
    TARGET_INVALID = TARGET_INVALID

    # Death
    PLAYER_DEATH = PLAYER_DEATH
    ENEMY_DEATH = ENEMY_DEATH
    CORPSE = CORPSE

    # UI elements
    BAR_TEXT = BAR_TEXT
    BAR_FILLED = BAR_FILLED
    BAR_EMPTY = BAR_EMPTY
    MENU_TITLE = MENU_TITLE
    MENU_TEXT = MENU_TEXT
    MENU_HIGHLIGHT = MENU_HIGHLIGHT
    WELCOME_TEXT = WELCOME_TEXT
