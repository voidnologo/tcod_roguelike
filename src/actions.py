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

    @property
    def target_actor(self):
        ''' Return the actor at this actions destination '''
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self):
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self):
        target = self.target_actor
        if not target:
            return

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f'{self.entity.name.capitalize()} attacks {target.name}'
        if damage > 0:
            print(f'{attack_desc} for {damage} hit points.')
            target.fighter.hp -= damage
        else:
            print(f'{attack_desc} does no damage.')


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

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class WaitAction(Action):
    def perform(self):
        pass
