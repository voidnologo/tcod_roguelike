from tcod.map import compute_fov
from input_handlers import MainGameEventHandler


class Engine:
    def __init__(self, player):
        self.event_handler = MainGameEventHandler(self)
        self.player = player

    def render(self, console, context):
        self.game_map.render(console)
        console.print(x=1, y=47, string=f'HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}')
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
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()
