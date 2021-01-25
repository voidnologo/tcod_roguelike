from actions.base_action import Action


class ItemAction(Action):
    def __init__(self, entity, item, target_xy=None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = (entity.x, entity.y)
        self.target_xy = target_xy

    @property
    def target_actor(self):
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self):
        """
        Invoke the items ability, thi action will be given as the context
        """
        self.item.consumable.activate(self)
