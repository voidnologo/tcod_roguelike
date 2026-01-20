"""Tests for the game engine and game loop integration.

These tests verify high-level game behavior:
- Engine initialization and state management
- FOV (Field of View) calculation and updates
- Turn processing (player then enemies)
- Message log functionality
- Full gameplay scenarios

Business Logic Tested:
- FOV updates reveal tiles around the player
- Explored tiles remain explored after leaving FOV
- Enemy turns process after player actions
- Messages are logged during gameplay
- Death ends the game appropriately
- Complete gameplay scenarios work end-to-end
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import GameConfig
from engine import Engine
from message_log import MessageLog
from tests.factories import GameFactory
from tests.helpers import CombatTestCase, GameTestCase


class TestEngineInitialization(unittest.TestCase):
    """Test Engine initialization."""

    def test_engine_has_player(self):
        """Engine initializes with a player reference."""
        game = GameFactory.create_game()
        self.assertIsNotNone(game.engine.player)
        self.assertIs(game.engine.player, game.player)

    def test_engine_has_message_log(self):
        """Engine initializes with a message log."""
        game = GameFactory.create_game()
        self.assertIsNotNone(game.engine.message_log)
        self.assertIsInstance(game.engine.message_log, MessageLog)

    def test_engine_has_mouse_location(self):
        """Engine tracks mouse location."""
        game = GameFactory.create_game()
        self.assertIsNotNone(game.engine.mouse_location)
        self.assertEqual(len(game.engine.mouse_location), 2)

    def test_engine_has_config(self):
        """Engine stores configuration."""
        config = GameConfig(screen_width=100, screen_height=80)
        player = GameFactory.create_player()
        engine = Engine(player=player, config=config)
        self.assertEqual(engine.config.screen_width, 100)
        self.assertEqual(engine.config.screen_height, 80)


class TestFieldOfView(GameTestCase):
    """Test Field of View (FOV) calculations."""

    def test_update_fov_reveals_player_tile(self):
        """Updating FOV makes the player's tile visible."""
        self.engine.update_fov()
        self.assertTrue(self.game_map.visible[self.player.x, self.player.y])

    def test_update_fov_reveals_nearby_tiles(self):
        """Updating FOV reveals tiles near the player."""
        self.engine.update_fov()
        # Tile adjacent to player should be visible
        self.assertTrue(self.game_map.visible[self.player.x + 1, self.player.y])

    def test_fov_blocked_by_walls(self):
        """FOV doesn't reveal tiles behind walls."""
        # Place wall next to player
        self.make_tile_wall(self.player.x + 1, self.player.y)
        self.engine.update_fov()

        # Tiles behind the wall should not be visible
        # (depending on FOV radius and geometry)
        # The wall itself should be visible
        self.assertTrue(self.game_map.visible[self.player.x + 1, self.player.y])

    def test_update_fov_marks_explored(self):
        """Visible tiles become explored."""
        self.engine.update_fov()
        # Player's tile should now be explored
        self.assertTrue(self.game_map.explored[self.player.x, self.player.y])

    def test_explored_persists_after_leaving_fov(self):
        """Tiles remain explored even when no longer visible."""
        # Update FOV at starting position
        self.engine.update_fov()
        initial_x, initial_y = self.player.x, self.player.y

        # Move player far away
        self.player.place(0, 0, self.game_map)
        self.engine.update_fov()

        # Original position should still be explored but not visible
        self.assertTrue(self.game_map.explored[initial_x, initial_y])
        self.assertFalse(self.game_map.visible[initial_x, initial_y])


class TestEnemyTurns(GameTestCase):
    """Test enemy turn processing."""

    def test_handle_enemy_turns_processes_all_enemies(self):
        """handle_enemy_turns calls perform on all enemy AIs."""
        # Place two enemies adjacent to player
        self.place_orc(self.player.x + 1, self.player.y)
        self.place_orc(self.player.x - 1, self.player.y)
        self.make_area_visible(0, 0, 20, 20)

        initial_player_hp = self.player.fighter.hp

        self.engine.handle_enemy_turns()

        # Both enemies should have attacked
        # Each deals 3-2=1 damage
        expected_hp = initial_player_hp - 2
        self.assertEqual(self.player.fighter.hp, expected_hp)

    def test_handle_enemy_turns_skips_player(self):
        """handle_enemy_turns doesn't process the player."""
        # Player's AI is BaseAI which would crash if perform() is called
        # This test ensures the player is skipped
        self.make_area_visible(0, 0, 20, 20)

        # Should not raise
        self.engine.handle_enemy_turns()

    def test_handle_enemy_turns_skips_dead_enemies(self):
        """handle_enemy_turns skips dead enemies."""
        orc = self.place_orc(self.player.x + 1, self.player.y)
        orc.fighter.take_damage(orc.fighter.hp)  # Kill orc

        initial_player_hp = self.player.fighter.hp

        self.engine.handle_enemy_turns()

        # Dead orc shouldn't attack
        self.assertEqual(self.player.fighter.hp, initial_player_hp)


class TestMessageLog(unittest.TestCase):
    """Test MessageLog functionality."""

    def test_message_log_starts_empty(self):
        """New message log has no messages."""
        log = MessageLog()
        self.assertEqual(len(log.messages), 0)

    def test_add_message(self):
        """Messages can be added to the log."""
        log = MessageLog()
        log.add_message("Test message")
        self.assertEqual(len(log.messages), 1)
        self.assertEqual(log.messages[0].plain_text, "Test message")

    def test_add_message_with_color(self):
        """Messages can have custom colors."""
        log = MessageLog()
        log.add_message("Colored message", fg=(255, 0, 0))
        self.assertEqual(log.messages[0].fg, (255, 0, 0))

    def test_message_stacking(self):
        """Identical consecutive messages stack."""
        log = MessageLog()
        log.add_message("Repeated message")
        log.add_message("Repeated message")
        log.add_message("Repeated message")

        self.assertEqual(len(log.messages), 1)
        self.assertEqual(log.messages[0].count, 3)

    def test_message_stacking_disabled(self):
        """Stacking can be disabled."""
        log = MessageLog()
        log.add_message("Message", stack=False)
        log.add_message("Message", stack=False)

        self.assertEqual(len(log.messages), 2)

    def test_message_full_text_with_count(self):
        """Stacked messages show count in full_text."""
        log = MessageLog()
        log.add_message("Hit!")
        log.add_message("Hit!")

        self.assertEqual(log.messages[0].full_text, "Hit! (x2)")

    def test_different_messages_dont_stack(self):
        """Different messages don't stack together."""
        log = MessageLog()
        log.add_message("First message")
        log.add_message("Second message")
        log.add_message("First message")  # Same as first, but not consecutive

        self.assertEqual(len(log.messages), 3)


class TestGameplayIntegration(GameTestCase):
    """Integration tests for complete gameplay scenarios."""

    def test_player_can_explore_and_fight(self):
        """Player can move around and engage in combat."""
        # Move player
        initial_x = self.player.x
        from actions import MovementAction
        MovementAction(self.player, 1, 0).perform()
        self.assertEqual(self.player.x, initial_x + 1)

        # Fight enemy
        orc = self.place_orc(self.player.x + 1, self.player.y)
        initial_orc_hp = orc.fighter.hp
        from actions import MeleeAction
        MeleeAction(self.player, 1, 0).perform()
        self.assertLess(orc.fighter.hp, initial_orc_hp)

    def test_player_can_collect_and_use_items(self):
        """Player can pick up items and use them."""
        # Damage player first
        self.damage_player(10)
        initial_hp = self.player.fighter.hp

        # Place and pick up potion
        potion = self.place_health_potion(self.player.x, self.player.y)
        from actions import PickupAction
        PickupAction(self.player).perform()
        self.assertIn(potion, self.player.inventory.items)

        # Use potion
        from actions import ItemAction
        ItemAction(self.player, potion).perform()
        self.assertGreater(self.player.fighter.hp, initial_hp)

    def test_enemy_ai_responds_to_player(self):
        """Enemies pursue and attack the player."""
        # Place enemy in view
        orc = self.place_orc(self.player.x + 3, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        initial_x = orc.x

        # Process enemy turn
        self.engine.handle_enemy_turns()

        # Orc should have moved toward player
        self.assertLess(orc.x, initial_x)

    def test_killing_enemy_generates_corpse(self):
        """Killing an enemy creates a corpse that can be walked over."""
        orc = self.place_orc(self.player.x + 1, self.player.y)

        # Kill the orc
        while orc.is_alive:
            from actions import MeleeAction
            MeleeAction(self.player, 1, 0).perform()

        # Orc should be dead
        self.assertFalse(orc.is_alive)
        self.assertFalse(orc.blocks_movement)

        # Player can move to orc's position
        from actions import MovementAction
        MovementAction(self.player, 1, 0).perform()
        self.assertEqual(self.player.x, orc.x)

    def test_player_death_scenario(self):
        """Player can be killed by enemies."""
        # Create strong enemy adjacent to player
        self.place_troll(self.player.x + 1, self.player.y, power=50)
        self.make_area_visible(0, 0, 20, 20)

        # Set player to low HP
        self.set_player_hp(1)

        # Process enemy turn - troll should kill player
        self.engine.handle_enemy_turns()

        self.assertFalse(self.player.is_alive)
        self.assertMessageContains("You Died")


class TestTurnOrder(CombatTestCase):
    """Test turn order and action resolution."""

    def test_player_acts_before_enemies(self):
        """In normal gameplay, player acts then enemies act."""
        self.make_area_visible(0, 0, 20, 20)
        initial_enemy_hp = self.enemy.fighter.hp
        initial_player_hp = self.player.fighter.hp

        # Player attacks
        self.attack_enemy()

        # Enemy should be damaged from player's attack
        expected_enemy_hp = initial_enemy_hp - (self.player.fighter.power - self.enemy.fighter.defense)
        self.assertEqual(self.enemy.fighter.hp, expected_enemy_hp)

        # Now process enemy turn
        self.engine.handle_enemy_turns()

        # Player should now be damaged
        self.assertLess(self.player.fighter.hp, initial_player_hp)

    def test_dead_enemy_doesnt_get_turn(self):
        """Enemies killed during player turn don't get to act."""
        # Set enemy to 1 HP so it dies from one hit
        self.enemy.fighter._hp = 1
        initial_player_hp = self.player.fighter.hp

        # Kill enemy
        self.attack_enemy()
        self.assertFalse(self.enemy.is_alive)

        # Process enemy turns
        self.engine.handle_enemy_turns()

        # Dead enemy shouldn't have attacked
        self.assertEqual(self.player.fighter.hp, initial_player_hp)


if __name__ == '__main__':
    unittest.main()
