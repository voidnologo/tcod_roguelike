from dataclasses import dataclass


@dataclass
class Entity:
    x: int
    y: int
    icon: str
    color: str

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def __hash__(self):
        return hash((self.x, self.y, self.icon))
