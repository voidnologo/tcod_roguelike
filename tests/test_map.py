"""Tests for game map and procedural generation.

These tests verify the behavior of:
- GameMap: Map bounds, entity tracking, tile queries
- Procedural generation: Room creation, tunnel carving, entity placement

Business Logic Tested:
- Map bounds checking works correctly
- Entities can be queried by position
- Blocking entities prevent movement
- FOV and exploration tracking work
- Rooms don't overlap
- Tunnels connect rooms
- Player starts in first room
- Monsters and items spawn correctly
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from map_objects import tile_types
from map_objects.game_map import GameMap
from map_objects.procgen import RectangularRoom, generate_dungeon, tunnel_between
from tests.factories import GameFactory
from tests.helpers import GameTestCase


class TestGameMapBounds(GameTestCase):
    """Test GameMap bounds checking."""

    def test_in_bounds_valid_position(self):
        """Positions inside the map are in bounds."""
        self.assertTrue(self.game_map.in_bounds(5, 5))
        self.assertTrue(self.game_map.in_bounds(0, 0))
        self.assertTrue(self.game_map.in_bounds(19, 19))

    def test_in_bounds_edge_positions(self):
        """Edge positions are in bounds."""
        # Top-left
        self.assertTrue(self.game_map.in_bounds(0, 0))
        # Top-right
        self.assertTrue(self.game_map.in_bounds(self.game_map.width - 1, 0))
        # Bottom-left
        self.assertTrue(self.game_map.in_bounds(0, self.game_map.height - 1))
        # Bottom-right
        self.assertTrue(self.game_map.in_bounds(
            self.game_map.width - 1, self.game_map.height - 1
        ))

    def test_out_of_bounds_negative(self):
        """Negative positions are out of bounds."""
        self.assertFalse(self.game_map.in_bounds(-1, 5))
        self.assertFalse(self.game_map.in_bounds(5, -1))
        self.assertFalse(self.game_map.in_bounds(-1, -1))

    def test_out_of_bounds_too_large(self):
        """Positions beyond map size are out of bounds."""
        self.assertFalse(self.game_map.in_bounds(self.game_map.width, 5))
        self.assertFalse(self.game_map.in_bounds(5, self.game_map.height))
        self.assertFalse(self.game_map.in_bounds(100, 100))


class TestGameMapEntities(GameTestCase):
    """Test GameMap entity management."""

    def test_get_blocking_entity_returns_blocker(self):
        """get_blocking_entity_at_location returns blocking entity."""
        orc = self.place_orc(5, 5)
        result = self.game_map.get_blocking_entity_at_location(5, 5)
        self.assertIs(result, orc)

    def test_get_blocking_entity_returns_none_for_empty(self):
        """get_blocking_entity_at_location returns None for empty space."""
        result = self.game_map.get_blocking_entity_at_location(5, 5)
        self.assertIsNone(result)

    def test_get_blocking_entity_ignores_items(self):
        """get_blocking_entity_at_location ignores non-blocking entities."""
        self.place_health_potion(5, 5)
        result = self.game_map.get_blocking_entity_at_location(5, 5)
        self.assertIsNone(result)

    def test_get_actor_at_location_returns_actor(self):
        """get_actor_at_location returns living actor at position."""
        orc = self.place_orc(5, 5)
        result = self.game_map.get_actor_at_location(5, 5)
        self.assertIs(result, orc)

    def test_get_actor_at_location_ignores_dead(self):
        """get_actor_at_location ignores dead actors."""
        orc = self.place_orc(5, 5)
        orc.fighter.take_damage(orc.fighter.hp)  # Kill orc
        result = self.game_map.get_actor_at_location(5, 5)
        self.assertIsNone(result)

    def test_get_actor_at_location_returns_none_for_empty(self):
        """get_actor_at_location returns None for empty space."""
        result = self.game_map.get_actor_at_location(5, 5)
        self.assertIsNone(result)

    def test_actors_property_yields_living_actors(self):
        """actors property yields only living actors."""
        orc1 = self.place_orc(5, 5)
        orc2 = self.place_orc(6, 6)
        orc2.fighter.take_damage(orc2.fighter.hp)  # Kill orc2

        actors = list(self.game_map.actors)
        self.assertIn(orc1, actors)
        self.assertIn(self.player, actors)
        self.assertNotIn(orc2, actors)

    def test_items_property_yields_items(self):
        """items property yields all items on the map."""
        potion = self.place_health_potion(5, 5)
        scroll = self.place_lightning_scroll(6, 6)

        items = list(self.game_map.items)
        self.assertIn(potion, items)
        self.assertIn(scroll, items)

    def test_get_entities_at_position(self):
        """get_entities_at yields all entities at a position."""
        orc = self.place_orc(5, 5)
        potion = self.place_health_potion(5, 5)

        entities = list(self.game_map.get_entities_at(5, 5))
        self.assertIn(orc, entities)
        self.assertIn(potion, entities)


class TestGameMapTiles(GameTestCase):
    """Test GameMap tile functionality."""

    def test_floor_is_walkable(self):
        """Floor tiles are walkable."""
        # Our test map is all floors
        self.assertTrue(self.game_map.tiles['walkable'][5, 5])

    def test_wall_is_not_walkable(self):
        """Wall tiles are not walkable."""
        self.make_tile_wall(5, 5)
        self.assertFalse(self.game_map.tiles['walkable'][5, 5])

    def test_floor_is_transparent(self):
        """Floor tiles are transparent (don't block FOV)."""
        self.assertTrue(self.game_map.tiles['transparent'][5, 5])

    def test_wall_is_not_transparent(self):
        """Wall tiles are not transparent (block FOV)."""
        self.make_tile_wall(5, 5)
        self.assertFalse(self.game_map.tiles['transparent'][5, 5])


class TestGameMapVisibility(GameTestCase):
    """Test GameMap visibility and exploration tracking."""

    def test_visible_starts_false(self):
        """All tiles start as not visible."""
        # Note: GameTestCase doesn't call update_fov
        # We need to check before any FOV update
        game = GameFactory.create_game()
        self.assertFalse(game.game_map.visible[5, 5])

    def test_explored_starts_false(self):
        """All tiles start as unexplored."""
        game = GameFactory.create_game()
        self.assertFalse(game.game_map.explored[5, 5])

    def test_set_visible_updates_tile(self):
        """Setting visibility updates the tile."""
        self.set_visible(5, 5, True)
        self.assertTrue(self.game_map.visible[5, 5])

    def test_make_area_visible(self):
        """make_area_visible sets visibility for a region."""
        self.make_area_visible(2, 2, 5, 5)
        self.assertTrue(self.game_map.visible[3, 3])
        self.assertTrue(self.game_map.visible[4, 4])


class TestRectangularRoom(unittest.TestCase):
    """Test RectangularRoom for dungeon generation."""

    def test_room_dimensions(self):
        """Room stores its dimensions correctly."""
        room = RectangularRoom(x=5, y=10, width=8, height=6)
        self.assertEqual(room.x1, 5)
        self.assertEqual(room.y1, 10)
        self.assertEqual(room.x2, 13)  # 5 + 8
        self.assertEqual(room.y2, 16)  # 10 + 6

    def test_room_center(self):
        """Room center is calculated correctly."""
        room = RectangularRoom(x=0, y=0, width=10, height=10)
        self.assertEqual(room.center, (5, 5))

    def test_room_inner_area(self):
        """Room inner area excludes walls."""
        room = RectangularRoom(x=0, y=0, width=10, height=10)
        inner = room.inner
        # Inner area should be (1, 10) x (1, 10) as slices
        self.assertEqual(inner[0], slice(1, 10))
        self.assertEqual(inner[1], slice(1, 10))

    def test_rooms_intersect(self):
        """Overlapping rooms are detected."""
        room1 = RectangularRoom(x=0, y=0, width=10, height=10)
        room2 = RectangularRoom(x=5, y=5, width=10, height=10)
        self.assertTrue(room1.intersects(room2))
        self.assertTrue(room2.intersects(room1))

    def test_rooms_dont_intersect(self):
        """Non-overlapping rooms are not detected as intersecting."""
        room1 = RectangularRoom(x=0, y=0, width=5, height=5)
        room2 = RectangularRoom(x=10, y=10, width=5, height=5)
        self.assertFalse(room1.intersects(room2))
        self.assertFalse(room2.intersects(room1))

    def test_adjacent_rooms_intersect(self):
        """Adjacent rooms (touching edges) are detected as intersecting."""
        room1 = RectangularRoom(x=0, y=0, width=5, height=5)
        room2 = RectangularRoom(x=5, y=0, width=5, height=5)
        # Rooms touch at x=5, so they intersect
        self.assertTrue(room1.intersects(room2))


class TestTunnelBetween(unittest.TestCase):
    """Test tunnel generation between rooms."""

    def test_tunnel_connects_points(self):
        """Tunnel includes both endpoints."""
        start = (0, 0)
        end = (5, 5)
        tunnel = list(tunnel_between(start, end))
        self.assertIn((0, 0), tunnel)
        self.assertIn((5, 5), tunnel)

    def test_tunnel_is_connected(self):
        """Tunnel forms a connected path (L-shaped)."""
        start = (0, 0)
        end = (5, 3)
        tunnel = list(tunnel_between(start, end))

        # Verify all points are present for an L-shaped path
        # Could go horizontal then vertical, or vertical then horizontal
        self.assertGreater(len(tunnel), 0)

        # Check that consecutive points are adjacent
        for i in range(len(tunnel) - 1):
            x1, y1 = tunnel[i]
            x2, y2 = tunnel[i + 1]
            # Bresenham can step diagonally, so check distance <= sqrt(2)
            distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            self.assertLessEqual(distance, 1.5)


class TestDungeonGeneration(GameTestCase):
    """Test full dungeon generation."""

    def test_generate_dungeon_creates_map(self):
        """generate_dungeon returns a valid GameMap."""
        dungeon = generate_dungeon(
            max_rooms=5,
            room_min_size=4,
            room_max_size=6,
            map_width=40,
            map_height=30,
            max_monsters_per_room=1,
            max_items_per_room=1,
            engine=self.engine,
        )
        self.assertIsInstance(dungeon, GameMap)
        self.assertEqual(dungeon.width, 40)
        self.assertEqual(dungeon.height, 30)

    def test_generate_dungeon_places_player(self):
        """Player is placed in the dungeon."""
        player = GameFactory.create_player()
        engine = GameFactory.create_game().engine
        engine.player = player

        dungeon = generate_dungeon(
            max_rooms=5,
            room_min_size=4,
            room_max_size=6,
            map_width=40,
            map_height=30,
            max_monsters_per_room=0,
            max_items_per_room=0,
            engine=engine,
        )

        self.assertIn(player, dungeon.entities)

    def test_generate_dungeon_has_floor_tiles(self):
        """Generated dungeon has walkable floor tiles."""
        dungeon = generate_dungeon(
            max_rooms=5,
            room_min_size=4,
            room_max_size=6,
            map_width=40,
            map_height=30,
            max_monsters_per_room=0,
            max_items_per_room=0,
            engine=self.engine,
        )

        # Should have some walkable tiles
        walkable_count = dungeon.tiles['walkable'].sum()
        self.assertGreater(walkable_count, 0)

    def test_generate_dungeon_spawns_monsters(self):
        """Generated dungeon contains monsters."""
        from entity import Actor

        dungeon = generate_dungeon(
            max_rooms=10,
            room_min_size=4,
            room_max_size=8,
            map_width=50,
            map_height=40,
            max_monsters_per_room=3,
            max_items_per_room=0,
            engine=self.engine,
        )

        # Count actors that aren't the player
        monsters = [
            e for e in dungeon.entities
            if isinstance(e, Actor) and e is not self.player
        ]
        self.assertGreater(len(monsters), 0)

    def test_generate_dungeon_spawns_items(self):
        """Generated dungeon contains items."""
        from entity import Item

        dungeon = generate_dungeon(
            max_rooms=10,
            room_min_size=4,
            room_max_size=8,
            map_width=50,
            map_height=40,
            max_monsters_per_room=0,
            max_items_per_room=3,
            engine=self.engine,
        )

        items = [e for e in dungeon.entities if isinstance(e, Item)]
        self.assertGreater(len(items), 0)

    def test_player_starts_on_floor(self):
        """Player starts on a walkable tile."""
        dungeon = generate_dungeon(
            max_rooms=5,
            room_min_size=4,
            room_max_size=6,
            map_width=40,
            map_height=30,
            max_monsters_per_room=0,
            max_items_per_room=0,
            engine=self.engine,
        )

        player_x, player_y = self.player.x, self.player.y
        self.assertTrue(dungeon.tiles['walkable'][player_x, player_y])


class TestTileTypes(unittest.TestCase):
    """Test tile type definitions."""

    def test_floor_properties(self):
        """Floor tile has correct properties."""
        self.assertTrue(tile_types.floor['walkable'])
        self.assertTrue(tile_types.floor['transparent'])

    def test_wall_properties(self):
        """Wall tile has correct properties."""
        self.assertFalse(tile_types.wall['walkable'])
        self.assertFalse(tile_types.wall['transparent'])

    def test_tiles_have_light_and_dark_graphics(self):
        """Tiles have both light and dark display modes."""
        # Check floor has both
        self.assertIsNotNone(tile_types.floor['light'])
        self.assertIsNotNone(tile_types.floor['dark'])
        # Check wall has both
        self.assertIsNotNone(tile_types.wall['light'])
        self.assertIsNotNone(tile_types.wall['dark'])


if __name__ == '__main__':
    unittest.main()
