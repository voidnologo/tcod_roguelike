"""Tests for action classes.

These tests verify the behavior of game actions:
- MovementAction: Moving entities around the map
- MeleeAction: Combat between actors
- BumpAction: Context-sensitive move or attack
- PickupAction: Collecting items
- ItemAction: Using items
- DropItemAction: Dropping items from inventory

Business Logic Tested:
- Movement is blocked by walls and other actors
- Melee attacks deal damage based on power minus defense
- Zero or negative damage still resolves (just deals no damage)
- Bump action automatically chooses move or attack
- Items can only be picked up at the same location
- Full inventory prevents picking up items
- Items are consumed after use (for consumables)
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import exceptions
from actions import (
    BumpAction,
    DropItemAction,
    ItemAction,
    MeleeAction,
    MovementAction,
    PickupAction,
    WaitAction,
)
from tests.factories import GameFactory
from tests.helpers import CombatTestCase, GameTestCase


class TestMovementAction(GameTestCase):
    """Test MovementAction behavior."""

    def test_movement_changes_position(self):
        """Moving updates the actor's coordinates."""
        initial_x, initial_y = self.player.x, self.player.y
        MovementAction(self.player, 1, 0).perform()
        self.assertPlayerAt(initial_x + 1, initial_y)

    def test_movement_in_all_directions(self):
        """Actors can move in all 8 directions."""
        directions = [
            (0, -1),   # North
            (1, -1),   # Northeast
            (1, 0),    # East
            (1, 1),    # Southeast
            (0, 1),    # South
            (-1, 1),   # Southwest
            (-1, 0),   # West
            (-1, -1),  # Northwest
        ]
        for dx, dy in directions:
            # Reset player position
            self.player.place(10, 10, self.game_map)
            MovementAction(self.player, dx, dy).perform()
            self.assertPlayerAt(10 + dx, 10 + dy)

    def test_movement_blocked_by_wall(self):
        """Moving into a wall raises ImpossibleActionError."""
        self.make_tile_wall(self.player.x + 1, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError) as ctx:
            MovementAction(self.player, 1, 0).perform()

        self.assertIn('blocked', str(ctx.exception).lower())

    def test_movement_blocked_by_actor(self):
        """Moving into another actor raises ImpossibleActionError."""
        self.place_orc(self.player.x + 1, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError) as ctx:
            MovementAction(self.player, 1, 0).perform()

        self.assertIn('blocked', str(ctx.exception).lower())

    def test_movement_blocked_by_map_edge(self):
        """Moving outside map bounds raises ImpossibleActionError."""
        self.player.place(0, 0, self.game_map)

        with self.assertRaises(exceptions.ImpossibleActionError):
            MovementAction(self.player, -1, 0).perform()

    def test_movement_over_item(self):
        """Actors can move over items (items don't block)."""
        self.place_health_potion(self.player.x + 1, self.player.y)
        initial_x = self.player.x

        MovementAction(self.player, 1, 0).perform()

        self.assertPlayerAt(initial_x + 1, self.player.y)

    def test_movement_over_corpse(self):
        """Actors can move over dead actors (corpses don't block)."""
        orc = self.place_orc(self.player.x + 1, self.player.y)
        # Kill the orc
        orc.fighter.take_damage(orc.fighter.hp)

        initial_x = self.player.x
        MovementAction(self.player, 1, 0).perform()

        self.assertPlayerAt(initial_x + 1, self.player.y)


class TestMeleeAction(CombatTestCase):
    """Test MeleeAction combat behavior."""

    def test_melee_attack_deals_damage(self):
        """Melee attack reduces target HP by (power - defense)."""
        initial_hp = self.enemy.fighter.hp
        expected_damage = self.player.fighter.power - self.enemy.fighter.defense

        self.attack_enemy()

        self.assertEqual(self.enemy.fighter.hp, initial_hp - expected_damage)

    def test_melee_attack_with_high_defense(self):
        """Attack against high defense deals no damage but still resolves."""
        # Remove the existing enemy
        self.game_map.entities.discard(self.enemy)

        # Create enemy with defense higher than player's power
        self.enemy = self.place_orc(
            self.player.x + 1, self.player.y,
            defense=self.player.fighter.power + 5
        )
        initial_hp = self.enemy.fighter.hp

        self.attack_enemy()

        # No damage dealt
        self.assertEqual(self.enemy.fighter.hp, initial_hp)
        # But message should be logged
        self.assertMessageContains('no damage')

    def test_melee_attack_logs_message(self):
        """Melee attack generates combat message."""
        self.attack_enemy()
        self.assertMessageContains('attacks')

    def test_melee_attack_on_empty_space_fails(self):
        """Attacking empty space raises ImpossibleActionError."""
        # Remove the enemy
        self.game_map.entities.discard(self.enemy)

        with self.assertRaises(exceptions.ImpossibleActionError) as ctx:
            MeleeAction(self.player, 1, 0).perform()

        self.assertIn('nothing to attack', str(ctx.exception).lower())

    def test_melee_attack_can_kill(self):
        """Melee attack that reduces HP to 0 kills target."""
        # Set enemy HP low enough to die in one hit
        self.enemy.fighter._hp = 1

        self.attack_enemy()

        self.assertEnemyDead()

    def test_enemy_melee_attack_damages_player(self):
        """Enemies can attack and damage the player."""
        initial_hp = self.player.fighter.hp
        expected_damage = self.enemy.fighter.power - self.player.fighter.defense

        self.enemy_attacks_player()

        self.assertPlayerHP(initial_hp - expected_damage)


class TestBumpAction(CombatTestCase):
    """Test BumpAction context-sensitive behavior.

    BumpAction is the primary action triggered by movement keys.
    It automatically attacks if bumping into an enemy, or moves otherwise.
    """

    def test_bump_into_enemy_attacks(self):
        """Bumping into an enemy triggers an attack."""
        initial_hp = self.enemy.fighter.hp

        BumpAction(self.player, 1, 0).perform()

        self.assertLess(self.enemy.fighter.hp, initial_hp)

    def test_bump_into_empty_space_moves(self):
        """Bumping into empty space moves the actor."""
        # Remove the enemy
        self.game_map.entities.discard(self.enemy)
        initial_x = self.player.x

        BumpAction(self.player, 1, 0).perform()

        self.assertEqual(self.player.x, initial_x + 1)

    def test_bump_into_wall_fails(self):
        """Bumping into a wall fails with error."""
        self.make_tile_wall(self.player.x - 1, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError):
            BumpAction(self.player, -1, 0).perform()

    def test_bump_attacks_not_moves_through_enemy(self):
        """Bumping into enemy attacks, doesn't move through them."""
        initial_x = self.player.x

        BumpAction(self.player, 1, 0).perform()

        # Player should not have moved
        self.assertEqual(self.player.x, initial_x)


class TestPickupAction(GameTestCase):
    """Test PickupAction item collection."""

    def test_pickup_adds_item_to_inventory(self):
        """Picking up an item adds it to inventory."""
        self.place_health_potion(self.player.x, self.player.y)

        PickupAction(self.player).perform()

        self.assertInventoryContains('Health Potion')

    def test_pickup_removes_item_from_map(self):
        """Picked up items are removed from the map."""
        potion = self.place_health_potion(self.player.x, self.player.y)

        PickupAction(self.player).perform()

        self.assertNotIn(potion, self.game_map.entities)

    def test_pickup_logs_message(self):
        """Picking up an item generates a message."""
        self.place_health_potion(self.player.x, self.player.y)

        PickupAction(self.player).perform()

        self.assertMessageContains('picked up')
        self.assertMessageContains('Health Potion')

    def test_pickup_nothing_fails(self):
        """Pickup with no item at location raises error."""
        with self.assertRaises(exceptions.ImpossibleActionError) as ctx:
            PickupAction(self.player).perform()

        self.assertIn('nothing', str(ctx.exception).lower())

    def test_pickup_full_inventory_fails(self):
        """Pickup with full inventory raises error."""
        # Fill inventory
        for _ in range(self.player.inventory.capacity):
            potion = GameFactory.create_health_potion()
            self.add_item_to_inventory(potion)

        # Place item to pick up
        self.place_health_potion(self.player.x, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError) as ctx:
            PickupAction(self.player).perform()

        self.assertIn('full', str(ctx.exception).lower())

    def test_pickup_chooses_item_at_player_position(self):
        """Pickup only gets items at the player's exact position."""
        # Place item away from player
        self.place_health_potion(self.player.x + 1, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError):
            PickupAction(self.player).perform()


class TestItemAction(GameTestCase):
    """Test ItemAction for using items."""

    def test_item_action_activates_consumable(self):
        """Using an item activates its consumable effect."""
        self.damage_player(10)
        initial_hp = self.player.fighter.hp

        potion = GameFactory.create_health_potion(heal_amount=5)
        self.add_item_to_inventory(potion)

        ItemAction(self.player, potion).perform()

        self.assertEqual(self.player.fighter.hp, initial_hp + 5)

    def test_item_action_with_target(self):
        """Item actions can specify a target location."""
        orc = self.place_orc(self.player.x + 2, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        initial_hp = orc.fighter.hp

        scroll = GameFactory.create_fireball_scroll(damage=10, radius=1)
        self.add_item_to_inventory(scroll)

        ItemAction(self.player, scroll, target_xy=(orc.x, orc.y)).perform()

        self.assertLess(orc.fighter.hp, initial_hp)


class TestDropItemAction(GameTestCase):
    """Test DropItemAction for dropping items."""

    def test_drop_removes_from_inventory(self):
        """Dropping an item removes it from inventory."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        DropItemAction(self.player, potion).perform()

        self.assertInventoryEmpty()

    def test_drop_places_item_on_map(self):
        """Dropped items appear on the map at player's position."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        DropItemAction(self.player, potion).perform()

        self.assertIn(potion, self.game_map.entities)
        self.assertEqual(potion.x, self.player.x)
        self.assertEqual(potion.y, self.player.y)


class TestWaitAction(GameTestCase):
    """Test WaitAction (skipping turn)."""

    def test_wait_does_nothing(self):
        """Wait action doesn't change player state."""
        initial_x, initial_y = self.player.x, self.player.y
        initial_hp = self.player.fighter.hp

        WaitAction(self.player).perform()

        self.assertPlayerAt(initial_x, initial_y)
        self.assertPlayerHP(initial_hp)

    def test_wait_succeeds(self):
        """Wait action completes without error."""
        # Should not raise
        WaitAction(self.player).perform()


class TestCombatDamageCalculation(CombatTestCase):
    """Test combat damage calculation rules.

    Damage formula: attacker.power - defender.defense
    Minimum damage: 0 (no negative damage/healing)
    """

    def test_damage_equals_power_minus_defense(self):
        """Damage dealt equals attacker power minus defender defense."""
        # Player: power 5, Enemy: defense 0 -> 5 damage
        initial_hp = self.enemy.fighter.hp
        self.attack_enemy()
        self.assertEqual(self.enemy.fighter.hp, initial_hp - 5)

    def test_defense_reduces_damage(self):
        """Higher defense reduces damage taken."""
        # Create enemy with higher defense
        tough_orc = self.place_troll(self.player.x - 1, self.player.y)
        # Troll has 1 defense, so damage is 5-1=4
        initial_hp = tough_orc.fighter.hp

        MeleeAction(self.player, -1, 0).perform()

        self.assertEqual(tough_orc.fighter.hp, initial_hp - 4)

    def test_high_power_deals_more_damage(self):
        """Higher power deals more damage."""
        # Create strong player
        strong_player = GameFactory.create_player(power=10)
        strong_player.place(self.player.x, self.player.y, self.game_map)

        initial_hp = self.enemy.fighter.hp
        # 10 power - 0 defense = 10 damage
        MeleeAction(strong_player, 1, 0).perform()

        self.assertEqual(self.enemy.fighter.hp, initial_hp - 10)


if __name__ == '__main__':
    unittest.main()
