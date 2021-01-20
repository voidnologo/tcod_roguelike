import tcod as libtcod

import input_handlers
from entity import Entity
from render_functions import render_all
from map_objects.game_map import GameMap


screen_width = 80
screen_height = 50
map_width = 80
map_height = 45
colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
}


def game_loop(console, context, entities, game_map):
    player = entities[0]
    console.clear()

    render_all(console, entities, game_map, screen_width, screen_height, colors)

    context.present(console)
    action = {}

    for event in libtcod.event.wait():
        context.convert_event(event)
        if event.type == 'QUIT':
            raise SystemExit()
        if event.type == 'KEYUP':
            action = input_handlers.handle_keys(event)

    if move := action.get('move'):
        dx, dy = move
        if not game_map.is_blocked(player.x + dx, player.y + dy):
            player.move(dx, dy)


def main():
    player = Entity(
        x=screen_width // 2,
        y=screen_height // 2,
        icon='@',
        color=libtcod.white,
    )
    npc = Entity(
        x=(screen_width // 2) - 5,
        y=(screen_height // 2),
        icon='X',
        color=libtcod.yellow,
    )

    entities = [player, npc]

    tileset = libtcod.tileset.load_tilesheet('arial10x10.png', 32, 8, libtcod.tileset.CHARMAP_TCOD)
    console = libtcod.Console(screen_width, screen_height, order='F')
    game_map = GameMap(map_width, map_height)

    with libtcod.context.new(columns=console.width, rows=console.height, tileset=tileset) as context:
        while True:
            game_loop(console, context, entities, game_map)


if __name__ == '__main__':
    main()
