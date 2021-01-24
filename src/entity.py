import copy
from dataclasses import dataclass


@dataclass
class Entity:
    x: int = 0
    y: int = 0
    icon: str = '?'
    color: str = (255, 255, 255)
    name: str = '<Unnamed>'
    blocks_movement: bool = False

    def spawn(self, gamemap, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.add(clone)
        return clone

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __hash__(self):
        return hash((self.x, self.y, self.icon))
