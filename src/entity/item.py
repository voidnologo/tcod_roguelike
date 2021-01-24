from entity.base_entity import Entity
from render_order import RenderOrder


class Item(Entity):
    def __init__(
        self,
        *,
        x=0,
        y=0,
        icon='?',
        color=(255, 255, 255),
        name='<Unnamed>',
        consumable=None,
    ):
        super().__init__(
            x=x,
            y=y,
            icon=icon,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.consumable.parent = self
