"""Test factories for creating common game objects.

These factories provide convenient methods to create fully-initialized game
objects for testing. They handle all the necessary wiring between components,
entities, and the game engine.

Usage:
    from tests.factories import GameFactory

    # Create a complete game setup
    game = GameFactory.create_game()

    # Access components
    player = game.player
    engine = game.engine
    game_map = game.game_map

    # Create and place entities
    orc = GameFactory.create_orc(game_map, x=5, y=5)
    potion = GameFactory.create_health_potion(game_map, x=3, y=3)
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from components.ai import BaseAI, HostileEnemy
from components.confusion_consumable import ConfusionConsumable
from components.fighter import Fighter
from components.fireball_damage_consumable import FireballDamageConsumable
from components.healing_consumable import HealingConsumable
from components.inventory import Inventory
from components.lightning_damage_consumable import LightningDamageConsumable
from config import DEFAULT_CONFIG, GameConfig
from engine import Engine
from entity import Actor, Item
from map_objects import tile_types
from map_objects.game_map import GameMap

if TYPE_CHECKING:
    pass


class TestGameMap(GameMap):
    """GameMap subclass for testing that doesn't have hardcoded tile placements."""

    def _initialize_tiles(self) -> np.ndarray:
        """Create initial tile array filled with walls (no hardcoded placements)."""
        return np.full(
            (self.width, self.height),
            fill_value=tile_types.wall,
            order='F',
        )


@dataclass
class GameSetup:
    """Container for a complete game setup used in tests.

    Attributes:
        engine: The game engine instance
        player: The player actor
        game_map: The game map

    Example:
        game = GameFactory.create_game()
        assert game.player.fighter.hp == 30
        assert game.engine.player is game.player
    """

    engine: Engine
    player: Actor
    game_map: GameMap


class GameFactory:
    """Factory for creating game objects in tests.

    This factory provides methods to create fully-wired game objects
    that are ready for testing. All objects are properly connected
    to the engine, game map, and each other.
    """

    # Default stats for test entities
    PLAYER_HP = 30
    PLAYER_DEFENSE = 2
    PLAYER_POWER = 5
    PLAYER_INVENTORY_CAPACITY = 26

    ORC_HP = 10
    ORC_DEFENSE = 0
    ORC_POWER = 3

    TROLL_HP = 16
    TROLL_DEFENSE = 1
    TROLL_POWER = 4

    @staticmethod
    def create_game(
        config: GameConfig = DEFAULT_CONFIG,
        map_width: int = 20,
        map_height: int = 20,
    ) -> GameSetup:
        """Create a complete game setup with engine, player, and map.

        Creates a minimal game environment suitable for testing. The map
        is initialized with all floor tiles for easy entity placement.

        Args:
            config: Game configuration to use
            map_width: Width of the test map
            map_height: Height of the test map

        Returns:
            GameSetup containing the engine, player, and game_map

        Example:
            game = GameFactory.create_game()
            game.player.move(1, 0)
            assert game.player.x == 1
        """
        player = GameFactory.create_player()
        engine = Engine(player=player, config=config)
        game_map = GameFactory.create_map(engine, map_width, map_height, entities=[player])
        engine.game_map = game_map
        player.place(map_width // 2, map_height // 2, game_map)
        return GameSetup(engine=engine, player=player, game_map=game_map)

    @staticmethod
    def create_player(
        x: int = 0,
        y: int = 0,
        hp: int | None = None,
        defense: int | None = None,
        power: int | None = None,
        inventory_capacity: int | None = None,
    ) -> Actor:
        """Create a player actor.

        Args:
            x: Initial x position
            y: Initial y position
            hp: Hit points (default: 30)
            defense: Defense stat (default: 2)
            power: Attack power (default: 5)
            inventory_capacity: Inventory size (default: 26)

        Returns:
            A new player Actor instance
        """
        return Actor(
            x=x,
            y=y,
            icon='@',
            color=(255, 128, 0),
            name='Player',
            ai_cls=BaseAI,
            fighter=Fighter(
                hp=hp if hp is not None else GameFactory.PLAYER_HP,
                defense=defense if defense is not None else GameFactory.PLAYER_DEFENSE,
                power=power if power is not None else GameFactory.PLAYER_POWER,
            ),
            inventory=Inventory(
                capacity=inventory_capacity if inventory_capacity is not None else GameFactory.PLAYER_INVENTORY_CAPACITY
            ),
        )

    @staticmethod
    def create_orc(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        hp: int | None = None,
        defense: int | None = None,
        power: int | None = None,
    ) -> Actor:
        """Create an orc enemy.

        Args:
            game_map: Optional map to place the orc on
            x: X position
            y: Y position
            hp: Hit points (default: 10)
            defense: Defense stat (default: 0)
            power: Attack power (default: 3)

        Returns:
            A new orc Actor instance
        """
        orc = Actor(
            x=x,
            y=y,
            icon='o',
            color=(63, 127, 63),
            name='Orc',
            ai_cls=HostileEnemy,
            fighter=Fighter(
                hp=hp if hp is not None else GameFactory.ORC_HP,
                defense=defense if defense is not None else GameFactory.ORC_DEFENSE,
                power=power if power is not None else GameFactory.ORC_POWER,
            ),
            inventory=Inventory(capacity=0),
        )
        if game_map:
            orc.place(x, y, game_map)
        return orc

    @staticmethod
    def create_troll(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        hp: int | None = None,
        defense: int | None = None,
        power: int | None = None,
    ) -> Actor:
        """Create a troll enemy.

        Args:
            game_map: Optional map to place the troll on
            x: X position
            y: Y position
            hp: Hit points (default: 16)
            defense: Defense stat (default: 1)
            power: Attack power (default: 4)

        Returns:
            A new troll Actor instance
        """
        troll = Actor(
            x=x,
            y=y,
            icon='T',
            color=(0, 127, 0),
            name='Troll',
            ai_cls=HostileEnemy,
            fighter=Fighter(
                hp=hp if hp is not None else GameFactory.TROLL_HP,
                defense=defense if defense is not None else GameFactory.TROLL_DEFENSE,
                power=power if power is not None else GameFactory.TROLL_POWER,
            ),
            inventory=Inventory(capacity=0),
        )
        if game_map:
            troll.place(x, y, game_map)
        return troll

    @staticmethod
    def create_health_potion(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        heal_amount: int = 4,
    ) -> Item:
        """Create a health potion item.

        Args:
            game_map: Optional map to place the potion on
            x: X position
            y: Y position
            heal_amount: Amount of HP restored when used

        Returns:
            A new health potion Item instance
        """
        potion = Item(
            x=x,
            y=y,
            icon='!',
            color=(128, 0, 128),
            name='Health Potion',
            consumable=HealingConsumable(amount=heal_amount),
        )
        if game_map:
            potion.place(x, y, game_map)
        return potion

    @staticmethod
    def create_lightning_scroll(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        damage: int = 20,
        maximum_range: int = 5,
    ) -> Item:
        """Create a lightning scroll item.

        Args:
            game_map: Optional map to place the scroll on
            x: X position
            y: Y position
            damage: Damage dealt to the target
            maximum_range: Maximum targeting range

        Returns:
            A new lightning scroll Item instance
        """
        scroll = Item(
            x=x,
            y=y,
            icon='~',
            color=(255, 165, 83),
            name='Lightning Scroll',
            consumable=LightningDamageConsumable(damage=damage, maximum_range=maximum_range),
        )
        if game_map:
            scroll.place(x, y, game_map)
        return scroll

    @staticmethod
    def create_confusion_scroll(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        number_of_turns: int = 10,
    ) -> Item:
        """Create a confusion scroll item.

        Args:
            game_map: Optional map to place the scroll on
            x: X position
            y: Y position
            number_of_turns: Duration of confusion effect

        Returns:
            A new confusion scroll Item instance
        """
        scroll = Item(
            x=x,
            y=y,
            icon='~',
            color=(207, 63, 255),
            name='Confusion Scroll',
            consumable=ConfusionConsumable(number_of_turns=number_of_turns),
        )
        if game_map:
            scroll.place(x, y, game_map)
        return scroll

    @staticmethod
    def create_fireball_scroll(
        game_map: GameMap | None = None,
        x: int = 0,
        y: int = 0,
        damage: int = 12,
        radius: int = 3,
    ) -> Item:
        """Create a fireball scroll item.

        Args:
            game_map: Optional map to place the scroll on
            x: X position
            y: Y position
            damage: Damage dealt in the area
            radius: Area of effect radius

        Returns:
            A new fireball scroll Item instance
        """
        scroll = Item(
            x=x,
            y=y,
            icon='~',
            color=(255, 0, 0),
            name='Fireball Scroll',
            consumable=FireballDamageConsumable(damage=damage, radius=radius),
        )
        if game_map:
            scroll.place(x, y, game_map)
        return scroll

    @staticmethod
    def create_map(
        engine: Engine,
        width: int = 20,
        height: int = 20,
        entities: list | None = None,
        fill_with_floor: bool = True,
    ) -> TestGameMap:
        """Create a game map for testing.

        Args:
            engine: The game engine
            width: Map width
            height: Map height
            entities: Initial entities to place
            fill_with_floor: If True, fill entire map with walkable floor tiles

        Returns:
            A new TestGameMap instance
        """
        game_map = TestGameMap(
            engine=engine,
            width=width,
            height=height,
            entities=entities or [],
        )
        if fill_with_floor:
            # Fill with floor tiles for easy testing
            game_map.tiles[:] = tile_types.floor
        return game_map

    @staticmethod
    def create_map_with_walls(
        engine: Engine,
        width: int = 20,
        height: int = 20,
        wall_positions: list[tuple[int, int]] | None = None,
        entities: list | None = None,
    ) -> TestGameMap:
        """Create a game map with specific wall positions.

        Args:
            engine: The game engine
            width: Map width
            height: Map height
            wall_positions: List of (x, y) positions for walls
            entities: Initial entities to place

        Returns:
            A new TestGameMap instance with walls at specified positions
        """
        game_map = GameFactory.create_map(
            engine=engine,
            width=width,
            height=height,
            entities=entities,
            fill_with_floor=True,
        )
        if wall_positions:
            for x, y in wall_positions:
                game_map.tiles[x, y] = tile_types.wall
        return game_map


class MessageLogHelper:
    """Helper for inspecting message log contents in tests.

    Example:
        game = GameFactory.create_game()
        game.engine.message_log.add_message("Test message")
        helper = MessageLogHelper(game.engine.message_log)
        assert helper.contains("Test")
        assert helper.last_message == "Test message"
    """

    def __init__(self, message_log):
        """Initialize with a MessageLog instance."""
        self.message_log = message_log

    @property
    def messages(self) -> list[str]:
        """Return all message texts."""
        return [m.plain_text for m in self.message_log.messages]

    @property
    def last_message(self) -> str | None:
        """Return the most recent message text."""
        if self.message_log.messages:
            return self.message_log.messages[-1].plain_text
        return None

    def contains(self, text: str) -> bool:
        """Check if any message contains the given text."""
        return any(text in msg for msg in self.messages)

    def count_containing(self, text: str) -> int:
        """Count messages containing the given text."""
        return sum(1 for msg in self.messages if text in msg)

    def clear(self) -> None:
        """Clear all messages."""
        self.message_log.messages.clear()
