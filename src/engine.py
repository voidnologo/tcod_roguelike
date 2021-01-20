import actions


class Engine:
    def __init__(self, entities, event_handler, player, game_map):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map

    def handle_events(self, events):
        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue

            if isinstance(action, actions.EscapeAction):
                actions.EscapeAction()

            if isinstance(action, actions.MovementAction):
                if not self.game_map.is_blocked(self.player.x + action.dx, self.player.y + action.dy):
                    self.player.move(action.dx, action.dy)

    def render(self, console, context):
        for entity in self.entities:
            console.print(entity.x, entity.y, entity.icon, fg=entity.color)
        context.present(console)
        console.clear()
