import copy

import tcod as libtcod

from engine import Engine
import entity_factories
from map_objects.procgen import generate_dungeon


screen_width = 80
screen_height = 50
map_width = 80
map_height = 45

room_max_size = 10
room_min_size = 6
max_rooms = 30

max_monsters_per_room = 2


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
        engine=engine,
    )
    engine.update_fov()

    with libtcod.context.new_terminal(
        columns=screen_width, rows=screen_height, tileset=tileset, title='Yet Another Roguelike', vsync=True
    ) as context:
        console = libtcod.Console(screen_width, screen_height, order='F')
        while True:
            engine.render(console=console, context=context)
            engine.event_handler.handle_events()


if __name__ == '__main__':
    main()
