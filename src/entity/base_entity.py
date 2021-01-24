import copy

from render_order import RenderOrder


class Entity:
    def __init__(
        self,
        parent=None,
        x=0,
        y=0,
        icon='?',
        color=(255, 255, 255),
        name='<Unnamed>',
        blocks_movement=False,
        render_order=RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.icon = icon
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            self.gamemap = parent
            parent.entities.add(self)

    @property
    def gamemap(self):
        return self.parent.gamemap

    def spawn(self, gamemap, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x, y, gamemap=None):
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, 'parent'):
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
