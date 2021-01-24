import color
import exceptions


class Action:
    def __init__(self, entity):
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
            raise exceptions.Impossible('Nothing to attack.')

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f'{self.entity.name.capitalize()} attacks {target.name}'
        attack_color = color.player_atk if self.entity is self.engine.player else color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f'{attack_desc} for {damage} hit points.', attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f'{attack_desc} does no damage.', attack_color)


class MovementAction(ActionWithDirection):
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # destination off of map
            raise exceptions.Impossible('That way is blocked.')
        if not self.engine.game_map.tiles['walkable'][dest_x, dest_y]:
            # destination blocked by a tile
            raise exceptions.Impossible('That way is blocked.')
        if self.blocking_entity:
            # destination blocked by a entity
            raise exceptions.Impossible('That way is blocked.')

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


class ItemAction(Action):
    def __init__(self, entity, item, target_xy=None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = (entity.x, entity.y)
        self.target_xy = target_xy

    @property
    def target_actor(self):
        return self.engine.game_map.get_actor_at_locatin(*self.target_xy)

    def perform(self):
        """
        Invoke the items ability, thi action will be given as the context
        """
        self.item.consumable.activate(self)


class PickupAction(Action):
    def perform(self):
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if inventory.full:
                    raise exceptions.Impossible('Your inventory is full.')
                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f'You picked up the {item.name}.')
                return
        raise exceptions.Impossible('There is nothing here to pick up.')
