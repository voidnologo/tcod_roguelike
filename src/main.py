import copy
import traceback

import tcod as libtcod

from engine import Engine
import entity_factories
import color
from map_objects.procgen import generate_dungeon


screen_width = 80
screen_height = 60
map_width = 80
map_height = 50

room_max_size = 10
room_min_size = 6
max_rooms = 30

max_monsters_per_room = 2
max_items_per_room = 2


def main():
    tileset = libtcod.tileset.load_tilesheet('dejavu10x10_gs_tc.png', 32, 8, libtcod.tileset.CHARMAP_TCOD)
    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        max_items_per_room=max_items_per_room,
        engine=engine,
    )
    engine.update_fov()
    engine.message_log.add_message(
        'Welcome to the next iteration of Super Dungeon Slaughter!', color.welcome_text
    )

    with libtcod.context.new_terminal(
        columns=screen_width, rows=screen_height, tileset=tileset, title='Yet Another Roguelike', vsync=True
    ) as context:
        console = libtcod.Console(screen_width, screen_height, order='F')
        while True:
            console.clear()
            engine.event_handler.on_render(console=console)
            context.present(console)
            try:
                for event in libtcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:
                traceback.print_exc()  # print errors to stderr
                # then print to message log
                engine.message_log.add_message(traceback.format_exc(), color.error)


if __name__ == '__main__':
    main()
