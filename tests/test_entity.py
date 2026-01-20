"""Tests for entity classes (Entity, Actor, Item).

These tests verify the behavior of game entities including:
- Basic entity properties and movement
- Actor-specific functionality (combat, AI, inventory)
- Item-specific functionality (consumables)

Business Logic Tested:
- Entities can be placed on the game map
- Entities can move and track their position
- Actors have a living/dead state based on AI presence
- Actors block movement, items do not
- Spawning creates independent copies of entities
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from entity.base_entity import Entity
from render_order import RenderOrder
from tests.factories import GameFactory
from tests.helpers import GameTestCase


class TestEntityBasics(GameTestCase):
    """Test basic Entity functionality."""

    def test_entity_has_position(self):
        """Entities track their x and y coordinates."""
        entity = Entity(x=5, y=10)
        self.assertEqual(entity.x, 5)
        self.assertEqual(entity.y, 10)
        self.assertEqual(entity.position, (5, 10))

    def test_entity_has_visual_properties(self):
        """Entities have icon, color, and name for display."""
        entity = Entity(icon='#', color=(255, 0, 0), name='Test Entity')
        self.assertEqual(entity.icon, '#')
        self.assertEqual(entity.color, (255, 0, 0))
        self.assertEqual(entity.name, 'Test Entity')

    def test_entity_default_values(self):
        """Entities have sensible defaults."""
        entity = Entity()
        self.assertEqual(entity.x, 0)
        self.assertEqual(entity.y, 0)
        self.assertEqual(entity.icon, '?')
        self.assertEqual(entity.name, '<Unnamed>')
        self.assertFalse(entity.blocks_movement)
        self.assertEqual(entity.render_order, RenderOrder.CORPSE)


class TestEntityMovement(GameTestCase):
    """Test entity movement functionality."""

    def test_move_changes_position(self):
        """Moving an entity updates its coordinates."""
        initial_x, initial_y = self.player.x, self.player.y
        self.player.move(1, 0)
        self.assertEqual(self.player.x, initial_x + 1)
        self.assertEqual(self.player.y, initial_y)

    def test_move_negative_direction(self):
        """Entities can move in negative directions."""
        initial_x, initial_y = self.player.x, self.player.y
        self.player.move(-1, -1)
        self.assertEqual(self.player.x, initial_x - 1)
        self.assertEqual(self.player.y, initial_y - 1)

    def test_move_diagonally(self):
        """Entities can move diagonally."""
        initial_x, initial_y = self.player.x, self.player.y
        self.player.move(1, 1)
        self.assertEqual(self.player.x, initial_x + 1)
        self.assertEqual(self.player.y, initial_y + 1)


class TestEntityDistance(GameTestCase):
    """Test entity distance calculations."""

    def test_distance_to_self_is_zero(self):
        """Distance from entity to its own position is zero."""
        distance = self.player.distance(self.player.x, self.player.y)
        self.assertEqual(distance, 0.0)

    def test_distance_horizontal(self):
        """Distance calculation works for horizontal displacement."""
        self.player.place(0, 0, self.game_map)
        distance = self.player.distance(3, 0)
        self.assertEqual(distance, 3.0)

    def test_distance_vertical(self):
        """Distance calculation works for vertical displacement."""
        self.player.place(0, 0, self.game_map)
        distance = self.player.distance(0, 4)
        self.assertEqual(distance, 4.0)

    def test_distance_diagonal(self):
        """Distance calculation uses Euclidean distance."""
        self.player.place(0, 0, self.game_map)
        distance = self.player.distance(3, 4)
        self.assertEqual(distance, 5.0)  # 3-4-5 triangle


class TestEntityPlacement(GameTestCase):
    """Test entity placement on the game map."""

    def test_place_updates_position(self):
        """Placing an entity updates its coordinates."""
        self.player.place(5, 7, self.game_map)
        self.assertPlayerAt(5, 7)

    def test_place_adds_to_map_entities(self):
        """Placing an entity adds it to the map's entity set."""
        orc = GameFactory.create_orc()
        orc.place(5, 5, self.game_map)
        self.assertIn(orc, self.game_map.entities)

    def test_place_on_new_map_removes_from_old(self):
        """Moving entity to new map removes it from the old map."""
        # Create a second map
        new_map = GameFactory.create_map(self.engine, 10, 10)

        # Create and place orc on first map
        orc = GameFactory.create_orc(self.game_map, 5, 5)
        self.assertIn(orc, self.game_map.entities)

        # Move to new map
        orc.place(3, 3, new_map)
        self.assertNotIn(orc, self.game_map.entities)
        self.assertIn(orc, new_map.entities)


class TestEntitySpawning(GameTestCase):
    """Test entity spawning creates independent copies."""

    def test_spawn_creates_copy(self):
        """Spawning creates a new entity instance."""
        orc_template = GameFactory.create_orc()
        spawned_orc = orc_template.spawn(self.game_map, 5, 5)
        self.assertIsNot(spawned_orc, orc_template)

    def test_spawn_at_specified_position(self):
        """Spawned entity appears at the specified location."""
        orc_template = GameFactory.create_orc()
        spawned_orc = orc_template.spawn(self.game_map, 7, 8)
        self.assertEqual(spawned_orc.x, 7)
        self.assertEqual(spawned_orc.y, 8)

    def test_spawn_adds_to_map(self):
        """Spawned entity is added to the game map."""
        orc_template = GameFactory.create_orc()
        spawned_orc = orc_template.spawn(self.game_map, 5, 5)
        self.assertIn(spawned_orc, self.game_map.entities)

    def test_spawned_entities_are_independent(self):
        """Changes to spawned entity don't affect original."""
        orc_template = GameFactory.create_orc(hp=10)
        spawned_orc = orc_template.spawn(self.game_map, 5, 5)

        # Damage the spawned orc
        spawned_orc.fighter.take_damage(5)

        # Original template should be unaffected
        self.assertEqual(orc_template.fighter.hp, 10)
        self.assertEqual(spawned_orc.fighter.hp, 5)


class TestActorProperties(GameTestCase):
    """Test Actor-specific properties and behavior."""

    def test_actor_blocks_movement(self):
        """Actors always block movement."""
        orc = self.place_orc(5, 5)
        self.assertTrue(orc.blocks_movement)

    def test_actor_has_actor_render_order(self):
        """Actors render above items and corpses."""
        orc = self.place_orc(5, 5)
        self.assertEqual(orc.render_order, RenderOrder.ACTOR)

    def test_actor_has_fighter_component(self):
        """Actors have a fighter component for combat."""
        self.assertIsNotNone(self.player.fighter)
        self.assertIsNotNone(self.player.fighter.hp)
        self.assertIsNotNone(self.player.fighter.defense)
        self.assertIsNotNone(self.player.fighter.power)

    def test_actor_has_inventory_component(self):
        """Actors have an inventory component."""
        self.assertIsNotNone(self.player.inventory)
        self.assertIsNotNone(self.player.inventory.capacity)

    def test_actor_has_ai_component(self):
        """Actors have an AI component that controls behavior."""
        orc = self.place_orc(5, 5)
        self.assertIsNotNone(orc.ai)


class TestActorAliveState(GameTestCase):
    """Test Actor alive/dead state tracking."""

    def test_actor_is_alive_with_ai(self):
        """Actors with AI are considered alive."""
        orc = self.place_orc(5, 5)
        self.assertTrue(orc.is_alive)

    def test_actor_is_dead_without_ai(self):
        """Actors without AI are considered dead."""
        orc = self.place_orc(5, 5)
        orc.ai = None
        self.assertFalse(orc.is_alive)

    def test_player_starts_alive(self):
        """The player starts in an alive state."""
        self.assertTrue(self.player.is_alive)


class TestItemProperties(GameTestCase):
    """Test Item-specific properties and behavior."""

    def test_item_does_not_block_movement(self):
        """Items do not block movement."""
        potion = self.place_health_potion(5, 5)
        self.assertFalse(potion.blocks_movement)

    def test_item_has_item_render_order(self):
        """Items render below actors."""
        potion = self.place_health_potion(5, 5)
        self.assertEqual(potion.render_order, RenderOrder.ITEM)

    def test_item_has_consumable_component(self):
        """Items have a consumable component."""
        potion = self.place_health_potion(5, 5)
        self.assertIsNotNone(potion.consumable)


class TestRenderOrder(unittest.TestCase):
    """Test render order values ensure correct layering."""

    def test_corpse_renders_below_item(self):
        """Corpses render below items."""
        self.assertLess(RenderOrder.CORPSE.value, RenderOrder.ITEM.value)

    def test_item_renders_below_actor(self):
        """Items render below actors."""
        self.assertLess(RenderOrder.ITEM.value, RenderOrder.ACTOR.value)


if __name__ == '__main__':
    unittest.main()
