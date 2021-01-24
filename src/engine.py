from tcod.map import compute_fov
from input_handlers import EventHandler


class Engine:
    def __init__(self, player):
        self.event_handler = EventHandler(self)
        self.player = player

    def render(self, console, context):
        self.game_map.render(console)
        context.present(console)
        console.clear()

    def update_fov(self):
        ''' recompute the visible area based on the players point of view '''
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=8,
        )
        # if a tile is "visible" add it to "explored"
        self.game_map.explored |= self.game_map.visible

    def handle_enemy_turns(self):
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wants to take a turn.')
