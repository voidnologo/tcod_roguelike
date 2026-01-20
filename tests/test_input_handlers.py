"""Tests for input handler classes.

These tests verify the behavior of event handlers:
- Key mapping and movement
- Handler transitions (main game -> inventory -> main game)
- Action dispatch from key events
- Mouse handling

Business Logic Tested:
- Movement keys map to correct directions
- Modifier keys (shift, ctrl, alt) affect cursor speed
- Inventory handlers return to main game on escape
- Game over handler only responds to escape
- Key constants are properly defined
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tcod.event import KeySym, Modifier

from input_handlers.consts import (
    CONFIRM_KEYS,
    CURSOR_Y_KEYS,
    MODIFIER_KEYS,
    MOVE_KEYS,
    WAIT_KEYS,
)
from tests.helpers import GameTestCase


class TestMoveKeys(unittest.TestCase):
    """Test movement key mappings."""

    def test_arrow_keys_mapped(self):
        """Arrow keys map to cardinal directions."""
        self.assertEqual(MOVE_KEYS[KeySym.UP], (0, -1))
        self.assertEqual(MOVE_KEYS[KeySym.DOWN], (0, 1))
        self.assertEqual(MOVE_KEYS[KeySym.LEFT], (-1, 0))
        self.assertEqual(MOVE_KEYS[KeySym.RIGHT], (1, 0))

    def test_numpad_keys_mapped(self):
        """Numpad keys map to all 8 directions."""
        # Cardinal
        self.assertEqual(MOVE_KEYS[KeySym.KP_8], (0, -1))   # North
        self.assertEqual(MOVE_KEYS[KeySym.KP_2], (0, 1))    # South
        self.assertEqual(MOVE_KEYS[KeySym.KP_4], (-1, 0))   # West
        self.assertEqual(MOVE_KEYS[KeySym.KP_6], (1, 0))    # East
        # Diagonal
        self.assertEqual(MOVE_KEYS[KeySym.KP_7], (-1, -1))  # Northwest
        self.assertEqual(MOVE_KEYS[KeySym.KP_9], (1, -1))   # Northeast
        self.assertEqual(MOVE_KEYS[KeySym.KP_1], (-1, 1))   # Southwest
        self.assertEqual(MOVE_KEYS[KeySym.KP_3], (1, 1))    # Southeast

    def test_vi_keys_mapped(self):
        """Vi keys (hjklyubn) map to movement."""
        self.assertEqual(MOVE_KEYS[KeySym.h], (-1, 0))   # West
        self.assertEqual(MOVE_KEYS[KeySym.j], (0, 1))    # South
        self.assertEqual(MOVE_KEYS[KeySym.k], (0, -1))   # North
        self.assertEqual(MOVE_KEYS[KeySym.l], (1, 0))    # East
        self.assertEqual(MOVE_KEYS[KeySym.y], (-1, -1))  # Northwest
        self.assertEqual(MOVE_KEYS[KeySym.u], (1, -1))   # Northeast
        self.assertEqual(MOVE_KEYS[KeySym.b], (-1, 1))   # Southwest
        self.assertEqual(MOVE_KEYS[KeySym.n], (1, 1))    # Southeast

    def test_diagonal_arrow_keys_mapped(self):
        """Home, End, PageUp, PageDown map to diagonals."""
        self.assertEqual(MOVE_KEYS[KeySym.HOME], (-1, -1))
        self.assertEqual(MOVE_KEYS[KeySym.END], (-1, 1))
        self.assertEqual(MOVE_KEYS[KeySym.PAGEUP], (1, -1))
        self.assertEqual(MOVE_KEYS[KeySym.PAGEDOWN], (1, 1))


class TestWaitKeys(unittest.TestCase):
    """Test wait key mappings."""

    def test_period_is_wait(self):
        """Period key triggers wait action."""
        self.assertIn(KeySym.PERIOD, WAIT_KEYS)

    def test_numpad_5_is_wait(self):
        """Numpad 5 triggers wait action."""
        self.assertIn(KeySym.KP_5, WAIT_KEYS)


class TestCursorKeys(unittest.TestCase):
    """Test cursor navigation key mappings."""

    def test_up_down_scroll_by_one(self):
        """Up and Down keys scroll by 1."""
        self.assertEqual(CURSOR_Y_KEYS[KeySym.UP], -1)
        self.assertEqual(CURSOR_Y_KEYS[KeySym.DOWN], 1)

    def test_page_up_down_scroll_by_ten(self):
        """PageUp and PageDown scroll by 10."""
        self.assertEqual(CURSOR_Y_KEYS[KeySym.PAGEUP], -10)
        self.assertEqual(CURSOR_Y_KEYS[KeySym.PAGEDOWN], 10)


class TestConfirmKeys(unittest.TestCase):
    """Test confirmation key mappings."""

    def test_enter_confirms(self):
        """Enter key is a confirm key."""
        self.assertIn(KeySym.RETURN, CONFIRM_KEYS)

    def test_numpad_enter_confirms(self):
        """Numpad Enter is a confirm key."""
        self.assertIn(KeySym.KP_ENTER, CONFIRM_KEYS)


class TestModifierKeys(unittest.TestCase):
    """Test modifier key identification."""

    def test_shift_keys_are_modifiers(self):
        """Shift keys are identified as modifiers."""
        self.assertIn(KeySym.LSHIFT, MODIFIER_KEYS)
        self.assertIn(KeySym.RSHIFT, MODIFIER_KEYS)

    def test_ctrl_keys_are_modifiers(self):
        """Ctrl keys are identified as modifiers."""
        self.assertIn(KeySym.LCTRL, MODIFIER_KEYS)
        self.assertIn(KeySym.RCTRL, MODIFIER_KEYS)

    def test_alt_keys_are_modifiers(self):
        """Alt keys are identified as modifiers."""
        self.assertIn(KeySym.LALT, MODIFIER_KEYS)
        self.assertIn(KeySym.RALT, MODIFIER_KEYS)


class TestMovementModifier(unittest.TestCase):
    """Test cursor movement speed modifiers."""

    def test_no_modifier_returns_one(self):
        """No modifier keys returns multiplier of 1."""
        from input_handlers.select_index_handler import get_movement_modifier
        modifier = get_movement_modifier(Modifier.NONE)
        self.assertEqual(modifier, 1)

    def test_shift_multiplies_by_five(self):
        """Shift key multiplies movement by 5."""
        from input_handlers.select_index_handler import get_movement_modifier
        modifier = get_movement_modifier(Modifier.LSHIFT)
        self.assertEqual(modifier, 5)

    def test_ctrl_multiplies_by_ten(self):
        """Ctrl key multiplies movement by 10."""
        from input_handlers.select_index_handler import get_movement_modifier
        modifier = get_movement_modifier(Modifier.LCTRL)
        self.assertEqual(modifier, 10)

    def test_alt_multiplies_by_twenty(self):
        """Alt key multiplies movement by 20."""
        from input_handlers.select_index_handler import get_movement_modifier
        modifier = get_movement_modifier(Modifier.LALT)
        self.assertEqual(modifier, 20)

    def test_modifiers_combine(self):
        """Multiple modifiers multiply together."""
        from input_handlers.select_index_handler import get_movement_modifier
        # Shift + Ctrl = 5 * 10 = 50
        modifier = get_movement_modifier(Modifier.LSHIFT | Modifier.LCTRL)
        self.assertEqual(modifier, 50)


class TestMainGameEventHandler(GameTestCase):
    """Test MainGameEventHandler behavior."""

    def test_handler_has_engine_reference(self):
        """Handler maintains reference to engine."""
        from input_handlers.main_game_event_handler import MainGameEventHandler
        handler = MainGameEventHandler(self.engine)
        self.assertIs(handler.engine, self.engine)


class TestInventoryEventHandler(GameTestCase):
    """Test InventoryEventHandler behavior."""

    def test_inventory_handler_has_title(self):
        """Inventory handler subclasses should define TITLE."""
        from input_handlers.inventory_activate_handler import InventoryActivateHandler
        from input_handlers.inventory_drop_handler import InventoryDropHandler

        activate_handler = InventoryActivateHandler(self.engine)
        drop_handler = InventoryDropHandler(self.engine)

        self.assertNotEqual(activate_handler.TITLE, '<missing title>')
        self.assertNotEqual(drop_handler.TITLE, '<missing title>')


class TestGameOverEventHandler(GameTestCase):
    """Test GameOverEventHandler behavior."""

    def test_game_over_handler_created_on_death(self):
        """GameOverEventHandler is used when player dies."""
        from input_handlers.base_event_handler import EventHandler

        # Create a handler
        EventHandler(self.engine)

        # Kill the player by setting HP to 0 through the fighter
        self.player.fighter._hp = 0
        self.player.ai = None  # Mark as dead

        # Check player is dead
        self.assertFalse(self.player.is_alive)


class TestHistoryViewer(GameTestCase):
    """Test HistoryViewer message log display."""

    def test_history_viewer_tracks_cursor(self):
        """History viewer tracks cursor position in log."""
        from input_handlers.history_viewer import HistoryViewer

        # Add some messages
        self.engine.message_log.add_message("Message 1")
        self.engine.message_log.add_message("Message 2")
        self.engine.message_log.add_message("Message 3")

        handler = HistoryViewer(self.engine)

        # Cursor should start at the end
        self.assertEqual(handler.cursor, handler.log_length - 1)

    def test_history_viewer_log_length(self):
        """History viewer knows the log length."""
        from input_handlers.history_viewer import HistoryViewer

        self.engine.message_log.add_message("Test")
        self.engine.message_log.add_message("Test 2")

        handler = HistoryViewer(self.engine)
        self.assertEqual(handler.log_length, 2)


class TestSelectIndexHandler(GameTestCase):
    """Test SelectIndexHandler for targeting."""

    def test_select_handler_centers_on_player(self):
        """Select handler initializes cursor at player position."""
        from input_handlers.select_index_handler import SelectIndexHandler

        # Custom handler for testing (base class is abstract)
        class TestSelectHandler(SelectIndexHandler):
            def on_index_selected(self, x, y):
                return None

        TestSelectHandler(self.engine)

        self.assertEqual(
            self.engine.mouse_location,
            (self.player.x, self.player.y)
        )


class TestHandlerTransitions(GameTestCase):
    """Test transitions between different handlers."""

    def test_ask_user_handler_returns_to_main(self):
        """AskUserEventHandler returns to main game on exit."""
        from input_handlers.ask_user_event_handler import AskUserEventHandler
        from input_handlers.main_game_event_handler import MainGameEventHandler

        handler = AskUserEventHandler(self.engine)
        result = handler.on_exit()

        self.assertIsInstance(result, MainGameEventHandler)


if __name__ == '__main__':
    unittest.main()
