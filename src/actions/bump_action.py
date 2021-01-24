from actions.action_with_direction import ActionWithDirection
from actions.melee_action import MeleeAction
from actions.movement_action import MovementAction


class BumpAction(ActionWithDirection):
    def perform(self):
        dest_x, dest_y = self.dest_xy

        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
