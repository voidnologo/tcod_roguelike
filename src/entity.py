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
