from components.base_component import BaseComponent


class Inventory(BaseComponent):
    parent = None

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def drop(self, item):
        """
        Removes an item from the inventory and adds to the game map
        """
        self.items.remove(item)
        item.place(self.parent.x, self.parent.y, self.gamemap)
        self.engine.message_log.add_message(f'You dropped the {item.name}.')

    @property
    def full(self):
        return len(self.items) >= self.capacity
