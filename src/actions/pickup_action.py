from actions.base_action import Action
import exceptions


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
