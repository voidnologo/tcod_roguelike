from tcod.map import compute_fov

from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location


class Engine:
    def __init__(self, player):
        self.event_handler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location = (0, 0)

    def render(self, console):
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=51, width=40, height=10)
        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            max_value=self.player.fighter.max_hp,
            total_width=20,
        )
        render_names_at_mouse_location(console, x=21, y=44, engine=self)

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
