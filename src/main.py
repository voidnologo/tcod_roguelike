"""Main entry point for the roguelike game."""

from __future__ import annotations

import copy
import traceback
from typing import TYPE_CHECKING

import tcod as libtcod

import color
import entity_factories
import exceptions
from config import DEFAULT_CONFIG, GameConfig
from engine import Engine
from input_handlers import EventHandler, MainGameEventHandler
from map_objects.procgen import generate_dungeon

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.context import Context

    from input_handlers.base_event_handler import BaseEventHandler


def game_loop(
    console: Console,
    context: Context,
    handler: BaseEventHandler,
) -> BaseEventHandler:
    """Process a single frame of the game loop."""
    console.clear()
    handler.on_render(console=console)
    context.present(console)

    try:
        for event in libtcod.event.wait():
            context.convert_event(event)
            handler = handler.handle_events(event)
    except Exception:
        traceback.print_exc()
        if isinstance(handler, EventHandler):
            handler.engine.message_log.add_message(traceback.format_exc(), color.error)

    return handler


def main(config: GameConfig = DEFAULT_CONFIG) -> None:
    """Initialize and run the game."""
    tileset = libtcod.tileset.load_tilesheet(
        'dejavu10x10_gs_tc.png', 32, 8, libtcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player, config=config)

    engine.game_map = generate_dungeon(
        max_rooms=config.max_rooms,
        room_min_size=config.room_min_size,
        room_max_size=config.room_max_size,
        map_width=config.map_width,
        map_height=config.map_height,
        max_monsters_per_room=config.max_monsters_per_room,
        max_items_per_room=config.max_items_per_room,
        engine=engine,
    )

    engine.update_fov()
    engine.message_log.add_message(
        'Welcome to the next iteration of Super Dungeon Slaughter!',
        color.welcome_text,
    )

    handler: BaseEventHandler = MainGameEventHandler(engine)

    with libtcod.context.new_terminal(
        columns=config.screen_width,
        rows=config.screen_height,
        tileset=tileset,
        title='Yet Another Roguelike',
        vsync=True,
    ) as context:
        console = libtcod.Console(config.screen_width, config.screen_height, order='F')

        try:
            while True:
                handler = game_loop(console, context, handler)
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            raise
        except BaseException:
            raise


if __name__ == '__main__':
    main()
