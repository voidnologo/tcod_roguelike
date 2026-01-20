# Development Standards

This document outlines the coding standards and conventions for the tcod_roguelike project.

## Python Version

- **Required:** Python 3.14+
- All files must include `from __future__ import annotations` at the top

## Type Annotations

### General Rules

- All public functions must have parameter and return type hints
- Use `TYPE_CHECKING` guards for imports that are only needed for type hints
- Prefer modern union syntax: `X | Y` over `Union[X, Y]`
- Prefer modern generic syntax: `list[int]` over `List[int]`

### Example

```python
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity.actor import Actor


def get_player(engine: Engine) -> Actor:
    """Return the player actor."""
    return engine.player
```

### Type Aliases

Common type aliases are defined in `src/game_types.py`:

```python
ColorRGB = tuple[int, int, int]
Position = tuple[int, int]
Direction = tuple[int, int]
```

## Dataclasses

### When to Use

- For immutable configuration: `@dataclass(frozen=True, slots=True)`
- For mutable state: `@dataclass(slots=True)`
- For simple data containers with few methods

### Example

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GameConfig:
    screen_width: int = 80
    screen_height: int = 60
```

## Match Statements

### When to Use

- Replace if/elif chains with 4+ branches
- Use for key event handling
- Use for pattern matching on enums

### Example

```python
match event.sym:
    case libtcod.event.K_ESCAPE:
        raise SystemExit()
    case libtcod.event.K_v:
        return HistoryViewer(self.engine)
    case _ if key in consts.MOVE_KEYS:
        dx, dy = consts.MOVE_KEYS[key]
        return actions.BumpAction(player, dx, dy)
    case _:
        return None
```

## Code Organization

### File Structure

```
src/
├── actions/           # Action classes for game commands
├── components/        # Component classes (Fighter, Inventory, AI)
│   └── ai/           # AI behavior components
├── entity/           # Entity classes (Actor, Item)
├── input_handlers/   # Event handlers for user input
├── map_objects/      # Map and dungeon generation
├── color.py          # Color definitions
├── config.py         # Game configuration
├── engine.py         # Main game engine
├── entity_factories.py # Entity templates and factories
├── exceptions.py     # Custom exceptions
├── game_types.py     # Type aliases
├── main.py           # Entry point
├── message_log.py    # Message log system
├── render_functions.py # UI rendering utilities
└── render_order.py   # Entity render order enum
```

### Import Order

1. Standard library imports
2. Third-party imports (tcod, numpy)
3. Local imports

### Module Docstrings

Every module should have a docstring describing its purpose:

```python
"""Procedural dungeon generation."""
```

## Error Handling

### Custom Exceptions

- Use `ImpossibleActionError` for actions that cannot be performed
- Use `QuitWithoutSaving` for clean exit without save
- Include descriptive messages with exceptions

### Example

```python
if not target:
    raise exceptions.ImpossibleActionError('Nothing to attack.')
```

## Component System

### BaseComponent

All components inherit from `BaseComponent` which provides:
- `parent`: Reference to the owning entity
- `engine`: Property to access the game engine
- `gamemap`: Property to access the current game map

### AI Components

AI classes inherit from `BaseAI` (which inherits from `BaseComponent`):
- Override `perform()` to define behavior
- Use `get_path_to()` for pathfinding

## Color System

### Organization

Colors are defined in `src/color.py`:

```python
from color import Colors

# Use semantic names
message_color = Colors.HEALTHY
attack_color = Colors.PLAYER_ATTACK

# Or use module-level constants
import color
message_color = color.health_recovered
```

### Adding New Colors

Add new colors to the appropriate section in `color.py` and include in the `Colors` class.

## Configuration

### GameConfig

Game settings are centralized in `src/config.py`:

```python
from config import DEFAULT_CONFIG, GameConfig

# Use default config
engine = Engine(player, config=DEFAULT_CONFIG)

# Or create custom config
custom_config = GameConfig(screen_width=100, screen_height=80)
```

## Testing

### Running Tests

The project uses Python's built-in `unittest` framework. **Do not use pytest.**

```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py -v

# Run specific test module
python run_tests.py test_entity

# Run specific test class
python run_tests.py test_entity.TestEntityBasics

# Run specific test method
python run_tests.py test_entity.TestEntityBasics.test_entity_has_position

# List all available tests
python run_tests.py --list

# Stop on first failure
python run_tests.py -f
```

### Test Organization

Tests are organized by the file/functionality they test:

```
tests/
├── __init__.py
├── factories.py          # Test factories for creating game objects
├── helpers.py            # Base test cases and utilities
├── test_entity.py        # Entity, Actor, Item tests
├── test_components.py    # Fighter, Inventory, AI, Consumable tests
├── test_actions.py       # Action classes tests
├── test_map.py           # GameMap and procedural generation tests
├── test_input_handlers.py# Input handler tests
└── test_engine.py        # Engine integration tests
```

### Writing Tests

#### Test Philosophy

- **Integration over unit**: Prefer testing from a user perspective
- **Tests as documentation**: Test names and docstrings explain business logic
- **Use factories**: Create objects with `GameFactory`, not raw constructors

#### Base Test Classes

Use the provided base classes for common setups:

```python
from tests.helpers import GameTestCase, CombatTestCase

class TestMyFeature(GameTestCase):
    """Test description explaining the business logic."""

    def test_player_can_do_something(self):
        """Players should be able to do X when Y."""
        # self.player, self.engine, self.game_map available
        self.player.move(1, 0)
        self.assertPlayerAt(11, 10)

class TestCombat(CombatTestCase):
    """Combat tests with an enemy pre-placed adjacent to player."""

    def test_attack_deals_damage(self):
        """Attacking an enemy should deal power minus defense damage."""
        # self.enemy is already adjacent to player
        initial_hp = self.enemy.fighter.hp
        self.attack_enemy()
        self.assertLess(self.enemy.fighter.hp, initial_hp)
```

#### Test Factories

Use `GameFactory` to create test objects:

```python
from tests.factories import GameFactory

# Create complete game setup
game = GameFactory.create_game()

# Create entities
player = GameFactory.create_player(hp=50, power=10)
orc = GameFactory.create_orc(game_map, x=5, y=5)
potion = GameFactory.create_health_potion(game_map, x=3, y=3)

# Create maps
game_map = GameFactory.create_map(engine, width=30, height=30)
game_map = GameFactory.create_map_with_walls(engine, wall_positions=[(5, 5), (6, 5)])
```

#### Custom Assertions

The `GameTestCase` class provides helpful assertions:

```python
self.assertPlayerAt(x, y)              # Check player position
self.assertPlayerHP(expected)           # Check player HP
self.assertMessageContains("text")      # Check message log
self.assertLastMessage("exact message") # Check last message
self.assertInventoryContains("item")    # Check inventory
self.assertInventoryEmpty()             # Check empty inventory
self.assertEntityAt(entity, x, y)       # Check entity position
```

#### Helper Methods

The base classes provide helper methods:

```python
# Place entities
orc = self.place_orc(5, 5)
potion = self.place_health_potion(3, 3)

# Modify player state
self.set_player_hp(10)
self.damage_player(5)
self.add_item_to_inventory(item)

# Modify map
self.make_tile_wall(5, 5)
self.make_tile_walkable(5, 5)
self.set_visible(5, 5, True)
self.make_area_visible(0, 0, 20, 20)
```

### Test Naming Conventions

- **Test classes**: `Test<Feature>` (e.g., `TestEntityMovement`)
- **Test methods**: `test_<what>_<expected>` (e.g., `test_move_changes_position`)
- **Docstrings**: Explain the business rule being tested

### Example Test

```python
class TestPickupAction(GameTestCase):
    """Test item collection from the game world.

    Business Logic:
    - Players can pick up items at their location
    - Items are removed from the map and added to inventory
    - Full inventory prevents pickup
    """

    def test_pickup_adds_item_to_inventory(self):
        """Picking up an item should add it to player's inventory."""
        potion = self.place_health_potion(self.player.x, self.player.y)

        PickupAction(self.player).perform()

        self.assertInventoryContains('Health Potion')

    def test_pickup_full_inventory_fails(self):
        """Cannot pick up items when inventory is full."""
        # Fill inventory to capacity
        for _ in range(self.player.inventory.capacity):
            self.add_item_to_inventory(GameFactory.create_health_potion())

        self.place_health_potion(self.player.x, self.player.y)

        with self.assertRaises(exceptions.ImpossibleActionError):
            PickupAction(self.player).perform()
```

### Manual Testing

After making changes:

1. Run test suite: `python run_tests.py`
2. Run linter: `ruff check src/`
3. Start the game: `python src/main.py`
4. Test basic actions:
   - Move around
   - Attack an enemy
   - Pick up an item
   - Use an item

## Naming Conventions

- **Classes:** PascalCase (`GameMap`, `BaseAI`)
- **Functions/Methods:** snake_case (`get_path_to`, `handle_events`)
- **Constants:** UPPER_SNAKE_CASE (`MOVE_KEYS`, `DEFAULT_CONFIG`)
- **Type Aliases:** PascalCase (`ColorRGB`, `Position`)
- **Private methods:** prefix with underscore (`_initialize_tiles`)

## DRY Principles

- Extract common patterns into helper functions
- Use data structures (spawn tables) instead of repeated conditionals
- Use base classes for shared behavior
- Consolidate duplicate error messages

## Generators

Use generators for iteration when:
- Iterating over filtered collections
- Lazy evaluation is beneficial
- Memory efficiency matters

```python
@property
def actors(self) -> Iterator[Actor]:
    yield from (
        entity for entity in self.entities
        if isinstance(entity, Actor) and entity.is_alive
    )
```
