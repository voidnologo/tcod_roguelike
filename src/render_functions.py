from itertools import product

import tcod as libtcod

import color


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


def render_bar(console, current_value, max_value, total_width):
    x_loc = 0
    y_loc = 51
    bar_width = int(float(current_value) / max_value * total_width)
    console.draw_rect(x=x_loc, y=y_loc, width=20, height=1, ch=1, bg=color.bar_empty)
    if bar_width > 0:
        console.draw_rect(x=x_loc, y=y_loc, width=bar_width, height=1, ch=1, bg=color.bar_filled)

    console.print(x=x_loc + 1, y=y_loc, string=f'HP: {current_value}/{max_value}', fg=color.bar_text)


def get_names_at_location(x, y, game_map):
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ''

    names = ', '.join(entity.name for entity in game_map.entities if entity.x == x and entity.y == y)
    return names.capitalize()


def render_names_at_mouse_location(console, x, y, engine):
    mouse_x, mouse_y = engine.mouse_location
    names_at_mouse_location = get_names_at_location(x=mouse_x, y=mouse_y, game_map=engine.game_map)
    console.print(x=x, y=y, string=names_at_mouse_location)
