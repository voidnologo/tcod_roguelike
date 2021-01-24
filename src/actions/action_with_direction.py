from actions.base_action import Action


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
