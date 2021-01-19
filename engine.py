from dataclasses import dataclass

import tcod as libtcod

import input_handlers


@dataclass
class Player:
    x: int
    y: int
    icon: str = '@'


def game_loop(console, context, player):
    console.clear()
    console.print(x=player.x, y=player.y, string=player.icon)
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
        player.x += dx
        player.y += dy


def main():
    screen_width = 80
    screen_height = 50
    player = Player(
        x=screen_width // 2,
        y=screen_height // 2,
    )

    tileset = libtcod.tileset.load_tilesheet('arial10x10.png', 32, 8, libtcod.tileset.CHARMAP_TCOD)
    console = libtcod.Console(screen_width, screen_height, order='F')

    with libtcod.context.new(columns=console.width, rows=console.height, tileset=tileset) as context:
        while True:
            game_loop(console, context, player)


if __name__ == '__main__':
    main()
