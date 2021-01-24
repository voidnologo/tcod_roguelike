from tcod.map import compute_fov


class Engine:
    def __init__(self, event_handler, player, game_map):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov()

    def handle_events(self, events):
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            action.perform(self, self.player)
            self.handle_enemy_turns()
            self.update_fov()  # update the FOV before the players next action

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
