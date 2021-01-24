from tcod.map import compute_fov


class Engine:
    def __init__(self, entities, event_handler, player, game_map):
        self.entities = entities
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
            self.update_fov()  # update the FOV before the players next action

    def render(self, console, context):
        self.game_map.render(console)
        for entity in self.entities:
            # only print entities in FOV
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.icon, fg=entity.color)
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
