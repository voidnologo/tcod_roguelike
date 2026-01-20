# Yet Another Roguelike
### *Super Dungeon Slaughter*

A classic roguelike dungeon crawler built with Python and the [tcod](https://python-tcod.readthedocs.io/en/latest/index.html) library. Descend into procedurally generated dungeons, battle orcs and trolls, collect magical scrolls, and try not to die horribly.

You *will* die horribly. That's the fun part.

---

## Table of Contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Controls](#controls)
- [Items & Magic](#items--magic)
- [Bestiary](#bestiary)
- [Credits & Resources](#credits--resources)
- [For Developers](#for-developers)

---

## Screenshots

**Exploring the dungeon:**
```
################################################################################
#......................#########################################################
#......................#########################################################
#......................#########################################################
#......................####################################.....................#
#......................####################################.....................#
#......................####################################........o............#
#......................+...................................+.....................#
#......................####################################.....................#
#......................####################################...........!.........#
######.#################################################################################
      #                                                    #.....................#
######+#######################                             #####################.#
#.........................+..#                                                 #.#
#.................@.......####            ~~~~~~~~~~~                    #######+#######
#.............T...........#               ~ LEGEND ~                     #.............#
#.........................#               ~~~~~~~~~~~                    #.............#
#.........................#               @ = You                        #.......%.....#
###########################               o = Orc                        #.............#
                                          T = Troll                      #.............#
                                          ! = Item                       ###############
                                          % = Corpse
                                          # = Wall
                                          . = Floor
                                          + = Tunnel
```

**Combat encounter:**
```
################################
#..............................#        HP: ||||||||||||........ 12/20
#..............................#
#..............@o..............#        --- Message Log ---
#..............................#        You kick the orc for 5 damage!
#..............................#        The orc attacks you for 3 damage.
#..............................#        You kick the orc for 5 damage!
#..............................#        The orc dies!
################################
```

**Casting a fireball:**
```
                      ************
                      *..........*
                      *....oo....*
                      *..........*
                      ************

            The fireball explodes, burning everything
            within 3 tiles for 12 damage!
```

---

## Features

- **Procedurally generated dungeons** - Every playthrough is unique with randomly generated rooms and tunnels
- **Permadeath** - When you die, you're dead. Start over and try again
- **Turn-based tactical combat** - Plan your moves carefully; enemies only act when you do
- **Field of view system** - Can't see around corners, and neither can your enemies
- **Fog of war** - Explored areas stay on your map, but you can't see what's lurking there now
- **Inventory management** - Carry up to 26 items and use them strategically
- **Multiple spell types** - Lightning bolts, fireballs, and confusion magic
- **Enemy AI** - Monsters hunt you down using pathfinding when they spot you

---

## Installation

### Prerequisites

- Python 3.10 or higher
- SDL2 library

### Installing SDL2

The tcod library requires SDL2 to be installed on your system.

**Arch Linux:**
```bash
sudo pacman -S sdl2
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install libsdl2-dev
```

**macOS:**
```bash
brew install sdl2
```

**Windows:**
SDL2 is typically bundled with tcod on Windows. If you encounter issues, download from [libsdl.org](https://www.libsdl.org/).

### Installing the Game

```bash
# Clone the repository
git clone https://github.com/yourusername/tcod_roguelike.git
cd tcod_roguelike

# Install dependencies
pip install -e .

# Run the game
python src/main.py
```

### macOS Big Sur Note

Numpy 1.19 had problems installing on macOS Big Sur. If you encounter issues:
- Install numpy binary directly, or:
  - `brew install openblas`
  - `OPENBLAS="$(brew --prefix openblas)" pip install numpy`

---

## How to Play

You are an adventurer who has entered a dungeon filled with hostile creatures. Your goal is simple: survive.

1. **Explore** - Move through rooms and tunnels to discover the dungeon layout
2. **Fight** - Walk into enemies to attack them (bump combat)
3. **Collect** - Pick up potions and scrolls to aid your survival
4. **Don't Die** - Manage your HP carefully; there are no second chances

The game is turn-based. Time only passes when you take an action, so take your time to think.

---

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / Numpad / `hjkl` | Move (8 directions) |
| `Home` `End` `PgUp` `PgDn` | Move diagonally |
| `.` or Numpad 5 | Wait (skip turn) |
| `g` | Pick up item |
| `i` | Open inventory |
| `d` | Drop item |
| `/` | Look mode |
| `v` | View message history |
| `Esc` | Quit / Cancel |

---

## Items & Magic

| Item | Effect |
|------|--------|
| **Health Potion** | Restores 4 HP instantly |
| **Lightning Scroll** | Strikes the nearest enemy within 5 tiles for 20 damage |
| **Confusion Scroll** | Target enemy stumbles around randomly for 10 turns |
| **Fireball Scroll** | Deals 12 damage to everything in a 3-tile radius (including you!) |

---

## Bestiary

| Creature | Symbol | HP | Power | Defense | Behavior |
|----------|--------|-----|-------|---------|----------|
| **Orc** | `o` | 10 | 3 | 0 | Common grunt, hunts on sight |
| **Troll** | `T` | 16 | 4 | 1 | Tougher, hits harder, takes more punishment |

---

## Credits & Resources

This project is based on the excellent [Roguelike Tutorial](http://rogueliketutorials.com/tutorials/tcod/v2/part-0/) - a fantastic resource for learning to build roguelikes with Python and tcod.

**Libraries:**
- [tcod (libtcod)](https://python-tcod.readthedocs.io/en/latest/index.html) - The Doryen Library for roguelike development
- [SDL2](https://www.libsdl.org/) - Cross-platform multimedia library

---

## For Developers

### Architecture Overview

The game uses a **component-based entity system**. Entities (player, monsters, items) are composed of reusable components like `Fighter` (combat stats), `Inventory` (item storage), and various `AI` behaviors. This makes it straightforward to add new entity types or modify existing ones.

**Action System:** All game commands are represented as `Action` objects with a `perform()` method. This cleanly separates intent from execution and makes it easy to have both player input and AI use the same action logic.

**Event Handlers:** Input processing uses a handler chain pattern that supports smooth state transitions between gameplay, inventory screens, and targeting modes.

### Project Structure

- `src/` - Main source code
  - `main.py` - Entry point and game loop
  - `engine.py` - Core game state and rendering
  - `actions/` - Action classes for all game commands
  - `components/` - Entity components (Fighter, Inventory, AI)
  - `entity/` - Entity classes (Actor, Item)
  - `map_objects/` - Dungeon generation and tile system
  - `input_handlers/` - Input processing and UI handlers
- `tests/` - Test suite using unittest

### Running Tests

```bash
python run_tests.py        # Run all tests
python run_tests.py -v     # Verbose output
```

### Key Configuration

Game parameters are centralized in `src/config.py` via a `GameConfig` dataclass - screen size, map dimensions, spawn rates, FOV radius, and UI layout are all easily tunable.

### Tech Stack

- Python 3.10+ with modern type hints throughout
- tcod for rendering, FOV calculation, and pathfinding
- NumPy for efficient tile map storage
- unittest for testing with custom test factories

---

*Now go forth and die gloriously in the dungeon!*
