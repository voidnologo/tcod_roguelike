import copy


class Entity:
    def __init__(
        self,
        gamemap=None,
        x=0,
        y=0,
        icon='?',
        color=(255, 255, 255),
        name='<Unnamed>',
        blocks_movement=False,
    ):
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        if gamemap:
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def spawn(self, gamemap, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x, y, gamemap=None):
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, 'gamemap'):
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
