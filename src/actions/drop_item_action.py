from actions.item_action import ItemAction


class DropItemAction(ItemAction):
    def perform(self):
        self.entity.inventory.drop(self.item)
