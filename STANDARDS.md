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

After making changes:

1. Run linter: `ruff check src/`
2. Start the game: `python src/main.py`
3. Test basic actions:
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
