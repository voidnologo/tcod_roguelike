import tcod as libtcod

from engine import Engine
from entity import Entity

from map_objects.game_map import GameMap
from input_handlers import EventHandler


screen_width = 80
screen_height = 50
map_width = 80
map_height = 45
colors = {
    'dark_wall': libtcod.Color(0, 0, 100),
    'dark_ground': libtcod.Color(50, 50, 150),
}


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

    tileset = libtcod.tileset.load_tilesheet('dejavu10x10_gs_tc.png', 32, 8, libtcod.tileset.CHARMAP_TCOD)
    game_map = GameMap(map_width, map_height)
    event_handler = EventHandler()
    entities = {player, npc}
    engine = Engine(
        entities=entities,
        event_handler=event_handler,
        player=player,
        game_map=game_map,
    )

    with libtcod.context.new_terminal(
        columns=screen_width, rows=screen_height, tileset=tileset, title='Yet Another Roguelike', vsync=True
    ) as context:
        console = libtcod.Console(screen_width, screen_height, order='F')
        while True:
            engine.render(console=console, context=context)
            events = libtcod.event.wait()
            engine.handle_events(events)


if __name__ == '__main__':
    main()
