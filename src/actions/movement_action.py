from actions.action_with_direction import ActionWithDirection
import exceptions


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
