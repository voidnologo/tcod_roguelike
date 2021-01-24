class Action:
    def perform(self, engine, entity):
        """
        Perform this action with the objects needed to determine its scope.
        `engine` is the scope this action is being performed in.
        `entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine, entity=None):
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx, dy):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine, entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.tiles['walkable'][dest_x, dest_y]:
            return

        entity.move(self.dx, self.dy)
