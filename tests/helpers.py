"""Test helpers and base test case classes.

This module provides base test case classes that set up common test fixtures
and provide utility methods for testing game functionality.

Usage:
    from tests.helpers import GameTestCase

    class TestMyFeature(GameTestCase):
        def test_something(self):
            # self.game, self.player, self.engine, self.game_map are available
            self.player.move(1, 0)
            self.assertEqual(self.player.x, 11)  # Started at center (10, 10)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from tests.factories import GameFactory, GameSetup, MessageLogHelper

if TYPE_CHECKING:
    from engine import Engine
    from entity.actor import Actor
    from map_objects.game_map import GameMap


class GameTestCase(unittest.TestCase):
    """Base test case with a complete game environment.

    Provides a fresh game setup for each test with:
    - self.game: The complete GameSetup object
    - self.player: The player actor
    - self.engine: The game engine
    - self.game_map: The game map (20x20, all floor tiles)
    - self.messages: MessageLogHelper for checking messages

    The player starts at position (10, 10) in the center of the map.

    Example:
        class TestPlayerMovement(GameTestCase):
            def test_player_can_move_right(self):
                initial_x = self.player.x
                self.player.move(1, 0)
                self.assertEqual(self.player.x, initial_x + 1)
    """

    game: GameSetup
    player: Actor
    engine: Engine
    game_map: GameMap
    messages: MessageLogHelper

    def setUp(self) -> None:
        """Create a fresh game environment before each test."""
        self.game = GameFactory.create_game()
        self.player = self.game.player
        self.engine = self.game.engine
        self.game_map = self.game.game_map
        self.messages = MessageLogHelper(self.engine.message_log)

    def place_orc(self, x: int, y: int, **kwargs) -> Actor:
        """Place an orc on the map at the given position.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_orc

        Returns:
            The created orc Actor
        """
        return GameFactory.create_orc(self.game_map, x, y, **kwargs)

    def place_troll(self, x: int, y: int, **kwargs) -> Actor:
        """Place a troll on the map at the given position.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_troll

        Returns:
            The created troll Actor
        """
        return GameFactory.create_troll(self.game_map, x, y, **kwargs)

    def place_health_potion(self, x: int, y: int, **kwargs):
        """Place a health potion on the map.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_health_potion

        Returns:
            The created health potion Item
        """
        return GameFactory.create_health_potion(self.game_map, x, y, **kwargs)

    def place_lightning_scroll(self, x: int, y: int, **kwargs):
        """Place a lightning scroll on the map.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_lightning_scroll

        Returns:
            The created lightning scroll Item
        """
        return GameFactory.create_lightning_scroll(self.game_map, x, y, **kwargs)

    def place_confusion_scroll(self, x: int, y: int, **kwargs):
        """Place a confusion scroll on the map.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_confusion_scroll

        Returns:
            The created confusion scroll Item
        """
        return GameFactory.create_confusion_scroll(self.game_map, x, y, **kwargs)

    def place_fireball_scroll(self, x: int, y: int, **kwargs):
        """Place a fireball scroll on the map.

        Args:
            x: X position
            y: Y position
            **kwargs: Additional arguments passed to create_fireball_scroll

        Returns:
            The created fireball scroll Item
        """
        return GameFactory.create_fireball_scroll(self.game_map, x, y, **kwargs)

    def add_item_to_inventory(self, item) -> None:
        """Add an item directly to the player's inventory.

        Args:
            item: The item to add
        """
        item.parent = self.player.inventory
        self.player.inventory.items.append(item)

    def set_player_hp(self, hp: int) -> None:
        """Set the player's current HP directly.

        Args:
            hp: The HP value to set
        """
        self.player.fighter._hp = hp

    def damage_player(self, amount: int) -> None:
        """Deal damage to the player.

        Args:
            amount: Amount of damage to deal
        """
        self.player.fighter.take_damage(amount)

    def make_tile_walkable(self, x: int, y: int) -> None:
        """Make a specific tile walkable.

        Args:
            x: X position
            y: Y position
        """
        from map_objects import tile_types
        self.game_map.tiles[x, y] = tile_types.floor

    def make_tile_wall(self, x: int, y: int) -> None:
        """Make a specific tile a wall.

        Args:
            x: X position
            y: Y position
        """
        from map_objects import tile_types
        self.game_map.tiles[x, y] = tile_types.wall

    def set_visible(self, x: int, y: int, visible: bool = True) -> None:
        """Set visibility for a specific tile.

        Args:
            x: X position
            y: Y position
            visible: Whether the tile should be visible
        """
        self.game_map.visible[x, y] = visible

    def make_area_visible(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """Make a rectangular area visible.

        Args:
            x1: Left bound
            y1: Top bound
            x2: Right bound (exclusive)
            y2: Bottom bound (exclusive)
        """
        self.game_map.visible[x1:x2, y1:y2] = True

    def assertMessageContains(self, text: str, msg: str | None = None) -> None:
        """Assert that any message contains the given text.

        Args:
            text: Text to search for
            msg: Optional failure message
        """
        if not self.messages.contains(text):
            failure_msg = msg or f"No message contains '{text}'. Messages: {self.messages.messages}"
            self.fail(failure_msg)

    def assertLastMessage(self, expected: str, msg: str | None = None) -> None:
        """Assert that the last message matches exactly.

        Args:
            expected: Expected message text
            msg: Optional failure message
        """
        actual = self.messages.last_message
        if actual != expected:
            failure_msg = msg or f"Expected last message '{expected}', got '{actual}'"
            self.fail(failure_msg)

    def assertPlayerAt(self, x: int, y: int, msg: str | None = None) -> None:
        """Assert that the player is at the given position.

        Args:
            x: Expected x position
            y: Expected y position
            msg: Optional failure message
        """
        if self.player.x != x or self.player.y != y:
            failure_msg = msg or f"Expected player at ({x}, {y}), got ({self.player.x}, {self.player.y})"
            self.fail(failure_msg)

    def assertPlayerHP(self, expected: int, msg: str | None = None) -> None:
        """Assert that the player has the expected HP.

        Args:
            expected: Expected HP value
            msg: Optional failure message
        """
        actual = self.player.fighter.hp
        if actual != expected:
            failure_msg = msg or f"Expected player HP {expected}, got {actual}"
            self.fail(failure_msg)

    def assertEntityAt(self, entity, x: int, y: int, msg: str | None = None) -> None:
        """Assert that an entity is at the given position.

        Args:
            entity: The entity to check
            x: Expected x position
            y: Expected y position
            msg: Optional failure message
        """
        if entity.x != x or entity.y != y:
            failure_msg = msg or f"Expected {entity.name} at ({x}, {y}), got ({entity.x}, {entity.y})"
            self.fail(failure_msg)

    def assertInventoryContains(self, item_name: str, msg: str | None = None) -> None:
        """Assert that the player's inventory contains an item with the given name.

        Args:
            item_name: Name of the item to find
            msg: Optional failure message
        """
        item_names = [item.name for item in self.player.inventory.items]
        if item_name not in item_names:
            failure_msg = msg or f"Item '{item_name}' not in inventory. Items: {item_names}"
            self.fail(failure_msg)

    def assertInventoryEmpty(self, msg: str | None = None) -> None:
        """Assert that the player's inventory is empty.

        Args:
            msg: Optional failure message
        """
        if self.player.inventory.items:
            item_names = [item.name for item in self.player.inventory.items]
            failure_msg = msg or f"Expected empty inventory, got: {item_names}"
            self.fail(failure_msg)


class CombatTestCase(GameTestCase):
    """Base test case for combat-related tests.

    Extends GameTestCase with additional helpers for combat scenarios.
    Creates an enemy adjacent to the player by default.

    Example:
        class TestMeleeAttack(CombatTestCase):
            def test_attack_deals_damage(self):
                initial_hp = self.enemy.fighter.hp
                self.attack_enemy()
                self.assertLess(self.enemy.fighter.hp, initial_hp)
    """

    enemy: Actor

    def setUp(self) -> None:
        """Create game with an enemy adjacent to the player."""
        super().setUp()
        # Place enemy one tile to the right of the player
        self.enemy = self.place_orc(self.player.x + 1, self.player.y)
        # Make the area visible so AI can see player
        self.make_area_visible(0, 0, 20, 20)

    def attack_enemy(self) -> None:
        """Perform a melee attack on the adjacent enemy."""
        from actions import MeleeAction
        dx = self.enemy.x - self.player.x
        dy = self.enemy.y - self.player.y
        MeleeAction(self.player, dx, dy).perform()

    def enemy_attacks_player(self) -> None:
        """Have the enemy attack the player."""
        from actions import MeleeAction
        dx = self.player.x - self.enemy.x
        dy = self.player.y - self.enemy.y
        MeleeAction(self.enemy, dx, dy).perform()

    def assertEnemyHP(self, expected: int, msg: str | None = None) -> None:
        """Assert that the enemy has the expected HP.

        Args:
            expected: Expected HP value
            msg: Optional failure message
        """
        actual = self.enemy.fighter.hp
        if actual != expected:
            failure_msg = msg or f"Expected enemy HP {expected}, got {actual}"
            self.fail(failure_msg)

    def assertEnemyAlive(self, msg: str | None = None) -> None:
        """Assert that the enemy is alive.

        Args:
            msg: Optional failure message
        """
        if not self.enemy.is_alive:
            failure_msg = msg or "Expected enemy to be alive"
            self.fail(failure_msg)

    def assertEnemyDead(self, msg: str | None = None) -> None:
        """Assert that the enemy is dead.

        Args:
            msg: Optional failure message
        """
        if self.enemy.is_alive:
            failure_msg = msg or "Expected enemy to be dead"
            self.fail(failure_msg)
