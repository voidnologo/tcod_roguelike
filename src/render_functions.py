from itertools import product
import tcod as libtcod


def render_all(console, entities, game_map, screen_width, screen_height, colors):
    render_map(console, game_map, colors)

    for entity in entities:
        draw_entity(console, entity)

    console.blit(console, 0, 0, screen_width, screen_height, 0, 0)


def render_map(console, game_map, colors):
    for y, x in product(range(game_map.height), range(game_map.width)):
        wall = game_map.tiles[x][y].block_sight
        if wall:
            libtcod.console_set_char_background(console, x, y, colors.get('dark_wall'))
        else:
            libtcod.console_set_char_background(console, x, y, colors.get('dark_ground'))


def clear_all(console, entities):
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity):
    console.print(entity.x, entity.y, entity.icon, entity.color)


def clear_entity(console, entity):
    console.print(entity.x, entity.y, '')
