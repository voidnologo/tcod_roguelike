class Action:
    def __init__(self, entity):
        super().__init__()
        self.entity = entity

    @property
    def engine(self):
        return self.entity.gamemap.engine

    def perform(self):
        """
        Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self):
        raise SystemExit()


class ActionWithDirection(Action):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self):
        return (self.entity.x + self.dx, self.entity.y + self.dy)

    @property
    def blocking_entity(self):
        ''' return the blocking entity at this actions destination '''
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self):
        target = self.blocking_entity
        if not target:
            return

        print(f'You kick the {target.name}, much to its annoyance!')  # TODO: implement attack


class MovementAction(ActionWithDirection):
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return  # destination off of map
        if not self.engine.game_map.tiles['walkable'][dest_x, dest_y]:
            return  # destination blocked by a tile
        if self.blocking_entity:
            return  # destination blocked by a entity

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if self.blocking_entity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
