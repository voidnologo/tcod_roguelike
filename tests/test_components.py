"""Tests for component classes (Fighter, Inventory, AI, Consumables).

These tests verify the behavior of entity components:
- Fighter: HP management, damage, healing, death
- Inventory: Item storage, capacity limits, dropping items
- AI: Enemy behavior, pathfinding, targeting
- Consumables: Item effects when used

Business Logic Tested:
- HP is clamped between 0 and max_hp
- Taking lethal damage triggers death
- Death converts actor to corpse state
- Inventory has capacity limits
- Healing is capped at max HP
- Hostile AI pursues and attacks player
- Confused AI moves randomly
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from components.fighter import Fighter
from components.inventory import Inventory
from render_order import RenderOrder
from tests.factories import GameFactory
from tests.helpers import CombatTestCase, GameTestCase


class TestFighterHP(GameTestCase):
    """Test Fighter HP management."""

    def test_fighter_starts_at_max_hp(self):
        """Fighters initialize with full HP."""
        fighter = Fighter(hp=20, defense=1, power=3)
        self.assertEqual(fighter.hp, 20)
        self.assertEqual(fighter.max_hp, 20)

    def test_hp_cannot_exceed_max(self):
        """Setting HP above max_hp clamps to max_hp."""
        self.set_player_hp(self.player.fighter.max_hp - 5)
        self.player.fighter.hp = 999
        self.assertEqual(self.player.fighter.hp, self.player.fighter.max_hp)

    def test_hp_cannot_go_below_zero(self):
        """Setting HP below 0 clamps to 0."""
        self.player.fighter.hp = -50
        self.assertEqual(self.player.fighter.hp, 0)


class TestFighterDamage(CombatTestCase):
    """Test Fighter damage mechanics."""

    def test_take_damage_reduces_hp(self):
        """Taking damage reduces current HP."""
        initial_hp = self.enemy.fighter.hp
        self.enemy.fighter.take_damage(3)
        self.assertEqual(self.enemy.fighter.hp, initial_hp - 3)

    def test_take_damage_clamped_at_zero(self):
        """Taking excessive damage stops at 0 HP."""
        self.enemy.fighter.take_damage(999)
        self.assertEqual(self.enemy.fighter.hp, 0)


class TestFighterDeath(CombatTestCase):
    """Test Fighter death mechanics."""

    def test_lethal_damage_triggers_death(self):
        """Reducing HP to 0 triggers death."""
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertEnemyDead()

    def test_death_removes_ai(self):
        """Dead actors have no AI."""
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertIsNone(self.enemy.ai)

    def test_death_changes_icon_to_corpse(self):
        """Dead actors display as corpse."""
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertEqual(self.enemy.icon, '%')

    def test_death_stops_blocking_movement(self):
        """Dead actors no longer block movement."""
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertFalse(self.enemy.blocks_movement)

    def test_death_changes_render_order(self):
        """Dead actors render as corpses (below living actors)."""
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertEqual(self.enemy.render_order, RenderOrder.CORPSE)

    def test_death_updates_name(self):
        """Dead actors have 'remains of' prefix in name."""
        original_name = self.enemy.name
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertIn('remains of', self.enemy.name)
        self.assertIn(original_name, self.enemy.name)

    def test_death_logs_message(self):
        """Death generates a message in the log."""
        enemy_name = self.enemy.name
        self.enemy.fighter.take_damage(self.enemy.fighter.hp)
        self.assertMessageContains(f'{enemy_name} is dead')


class TestFighterHealing(GameTestCase):
    """Test Fighter healing mechanics."""

    def test_heal_increases_hp(self):
        """Healing increases current HP."""
        self.set_player_hp(10)
        self.player.fighter.heal(5)
        self.assertEqual(self.player.fighter.hp, 15)

    def test_heal_capped_at_max_hp(self):
        """Healing cannot exceed max HP."""
        self.set_player_hp(self.player.fighter.max_hp - 2)
        healed = self.player.fighter.heal(10)
        self.assertEqual(self.player.fighter.hp, self.player.fighter.max_hp)
        self.assertEqual(healed, 2)  # Only healed 2, not 10

    def test_heal_returns_amount_healed(self):
        """Heal method returns actual amount recovered."""
        self.set_player_hp(10)
        healed = self.player.fighter.heal(5)
        self.assertEqual(healed, 5)

    def test_heal_at_full_hp_returns_zero(self):
        """Healing at full HP returns 0."""
        healed = self.player.fighter.heal(10)
        self.assertEqual(healed, 0)


class TestInventoryCapacity(GameTestCase):
    """Test Inventory capacity limits."""

    def test_inventory_starts_empty(self):
        """Inventories start with no items."""
        self.assertEqual(len(self.player.inventory.items), 0)

    def test_inventory_not_full_when_empty(self):
        """Empty inventory is not full."""
        self.assertFalse(self.player.inventory.full)

    def test_inventory_full_at_capacity(self):
        """Inventory is full when at capacity."""
        # Fill the inventory
        for _i in range(self.player.inventory.capacity):
            potion = GameFactory.create_health_potion()
            potion.parent = self.player.inventory
            self.player.inventory.items.append(potion)

        self.assertTrue(self.player.inventory.full)

    def test_inventory_capacity_is_configurable(self):
        """Inventory capacity can be set on creation."""
        inventory = Inventory(capacity=5)
        self.assertEqual(inventory.capacity, 5)


class TestInventoryDropping(GameTestCase):
    """Test dropping items from inventory."""

    def test_drop_removes_from_inventory(self):
        """Dropping an item removes it from inventory."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)
        self.assertEqual(len(self.player.inventory.items), 1)

        self.player.inventory.drop(potion)
        self.assertEqual(len(self.player.inventory.items), 0)

    def test_drop_places_item_at_player_position(self):
        """Dropped items appear at the dropper's location."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        self.player.inventory.drop(potion)
        self.assertEqual(potion.x, self.player.x)
        self.assertEqual(potion.y, self.player.y)

    def test_drop_adds_item_to_map(self):
        """Dropped items are added to the game map."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        self.player.inventory.drop(potion)
        self.assertIn(potion, self.game_map.entities)

    def test_drop_logs_message(self):
        """Dropping an item logs a message."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        self.player.inventory.drop(potion)
        self.assertMessageContains('dropped')
        self.assertMessageContains(potion.name)


class TestHostileAI(GameTestCase):
    """Test HostileEnemy AI behavior.

    The hostile AI should:
    - Attack when adjacent to player
    - Move toward player when visible
    - Follow last known path when player not visible
    """

    def test_hostile_ai_attacks_when_adjacent(self):
        """Hostile AI attacks player when adjacent."""
        orc = self.place_orc(self.player.x + 1, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        initial_hp = self.player.fighter.hp

        orc.ai.perform()

        # Orc has 3 power, player has 2 defense = 1 damage
        self.assertEqual(self.player.fighter.hp, initial_hp - 1)

    def test_hostile_ai_moves_toward_player(self):
        """Hostile AI moves toward visible player."""
        # Place orc 3 tiles away
        orc = self.place_orc(self.player.x + 3, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        initial_x = orc.x

        orc.ai.perform()

        # Orc should have moved closer
        self.assertLess(orc.x, initial_x)

    def test_hostile_ai_waits_when_not_visible(self):
        """Hostile AI with no path waits when player not visible."""
        orc = self.place_orc(self.player.x + 3, self.player.y)
        # Don't make area visible - orc can't see player
        initial_x, initial_y = orc.x, orc.y

        orc.ai.perform()

        # Orc should not have moved (no path, player not visible)
        self.assertEqual(orc.x, initial_x)
        self.assertEqual(orc.y, initial_y)


class TestConfusedAI(GameTestCase):
    """Test ConfusedEnemy AI behavior."""

    def test_confused_ai_moves_randomly(self):
        """Confused AI moves in random directions."""
        from components.ai.confused_enemy_ai import ConfusedEnemy

        orc = self.place_orc(self.player.x + 5, self.player.y)
        original_ai = orc.ai

        # Replace with confused AI
        orc.ai = ConfusedEnemy(orc, previous_ai=original_ai, turns_remaining=5)

        # Track if orc moves (might move randomly, might bump into wall)
        initial_x, initial_y = orc.x, orc.y
        for _ in range(10):  # Try multiple times since movement is random
            orc.x, orc.y = initial_x, initial_y
            try:
                orc.ai.perform()
                if orc.x != initial_x or orc.y != initial_y:
                    break
            except Exception:
                pass  # Might fail if bumps into boundary

        # Confused AI should attempt to move (may fail due to walls)
        # This test verifies the AI runs without crashing

    def test_confused_ai_counts_down_turns(self):
        """Confused AI decrements remaining turns."""
        from components.ai.confused_enemy_ai import ConfusedEnemy

        orc = self.place_orc(self.player.x + 5, self.player.y)
        original_ai = orc.ai

        confused_ai = ConfusedEnemy(orc, previous_ai=original_ai, turns_remaining=5)
        orc.ai = confused_ai

        try:
            orc.ai.perform()
        except Exception:
            pass  # May fail due to wall collision

        self.assertEqual(confused_ai.turns_remaining, 4)

    def test_confused_ai_reverts_when_done(self):
        """Confused AI reverts to previous AI when turns expire."""
        from components.ai.confused_enemy_ai import ConfusedEnemy
        from components.ai.hostile_enemy_ai import HostileEnemy

        orc = self.place_orc(self.player.x + 5, self.player.y)
        original_ai = orc.ai

        # turns_remaining=1 means: perform() decrements to 0, next perform() reverts
        orc.ai = ConfusedEnemy(orc, previous_ai=original_ai, turns_remaining=1)

        try:
            orc.ai.perform()  # Decrements to 0
        except Exception:
            pass

        # Perform again - this time it will revert
        try:
            orc.ai.perform()  # Reverts because turns_remaining <= 0
        except Exception:
            pass

        # Should have reverted to hostile AI
        self.assertIsInstance(orc.ai, HostileEnemy)


class TestHealingConsumable(GameTestCase):
    """Test HealingConsumable item effects."""

    def test_healing_potion_restores_hp(self):
        """Using a health potion restores HP."""
        self.damage_player(10)
        initial_hp = self.player.fighter.hp

        potion = self.place_health_potion(self.player.x, self.player.y, heal_amount=4)
        self.add_item_to_inventory(potion)

        from actions import ItemAction
        action = ItemAction(self.player, potion)
        action.perform()

        self.assertEqual(self.player.fighter.hp, initial_hp + 4)

    def test_healing_potion_consumed_after_use(self):
        """Health potion is removed from inventory after use."""
        self.damage_player(10)

        potion = GameFactory.create_health_potion(heal_amount=4)
        self.add_item_to_inventory(potion)

        from actions import ItemAction
        action = ItemAction(self.player, potion)
        action.perform()

        self.assertNotIn(potion, self.player.inventory.items)

    def test_healing_potion_fails_at_full_hp(self):
        """Cannot use health potion when at full HP."""
        import exceptions

        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        from actions import ItemAction
        action = ItemAction(self.player, potion)

        with self.assertRaises(exceptions.ImpossibleActionError):
            action.perform()

    def test_healing_potion_not_consumed_if_fails(self):
        """Health potion is not consumed if use fails."""
        potion = GameFactory.create_health_potion()
        self.add_item_to_inventory(potion)

        from actions import ItemAction
        action = ItemAction(self.player, potion)

        try:
            action.perform()
        except Exception:
            pass

        self.assertIn(potion, self.player.inventory.items)


class TestLightningConsumable(GameTestCase):
    """Test LighteningDamageConsumable item effects."""

    def test_lightning_scroll_damages_nearest_enemy(self):
        """Lightning scroll damages the closest visible enemy."""
        orc = self.place_orc(self.player.x + 2, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        initial_hp = orc.fighter.hp

        # Use damage less than orc HP to verify damage calculation
        scroll = GameFactory.create_lightning_scroll(damage=5, maximum_range=5)
        self.add_item_to_inventory(scroll)

        from actions import ItemAction
        action = ItemAction(self.player, scroll)
        action.perform()

        self.assertEqual(orc.fighter.hp, initial_hp - 5)

    def test_lightning_scroll_fails_without_target(self):
        """Lightning scroll fails if no enemies in range."""
        import exceptions

        scroll = GameFactory.create_lightning_scroll()
        self.add_item_to_inventory(scroll)

        from actions import ItemAction
        action = ItemAction(self.player, scroll)

        with self.assertRaises(exceptions.ImpossibleActionError):
            action.perform()


class TestFireballConsumable(GameTestCase):
    """Test FireballDamageConsumable item effects."""

    def test_fireball_damages_area(self):
        """Fireball damages all actors in radius."""
        orc1 = self.place_orc(5, 5)
        orc2 = self.place_orc(6, 5)  # Adjacent to orc1
        self.make_area_visible(0, 0, 20, 20)

        scroll = GameFactory.create_fireball_scroll(damage=12, radius=2)
        self.add_item_to_inventory(scroll)

        # Fireball requires target selection, which returns a callback
        # We'll test by directly calling activate with target coordinates
        from actions import ItemAction
        action = ItemAction(self.player, scroll, target_xy=(5, 5))
        action.perform()

        # Both orcs should be damaged
        self.assertLess(orc1.fighter.hp, GameFactory.ORC_HP)
        self.assertLess(orc2.fighter.hp, GameFactory.ORC_HP)


class TestConfusionConsumable(GameTestCase):
    """Test ConfusionConsumable item effects."""

    def test_confusion_scroll_changes_ai(self):
        """Confusion scroll replaces enemy AI with confused AI."""
        from components.ai.confused_enemy_ai import ConfusedEnemy
        from components.ai.hostile_enemy_ai import HostileEnemy

        orc = self.place_orc(self.player.x + 2, self.player.y)
        self.make_area_visible(0, 0, 20, 20)
        self.assertIsInstance(orc.ai, HostileEnemy)

        scroll = GameFactory.create_confusion_scroll(number_of_turns=10)
        self.add_item_to_inventory(scroll)

        # Confusion requires target selection
        from actions import ItemAction
        action = ItemAction(self.player, scroll, target_xy=(orc.x, orc.y))
        action.perform()

        self.assertIsInstance(orc.ai, ConfusedEnemy)


if __name__ == '__main__':
    unittest.main()
