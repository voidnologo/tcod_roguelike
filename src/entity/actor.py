from entity.base_entity import Entity
from render_order import RenderOrder


class Actor(Entity):
    def __init__(
        self,
        *,
        x=0,
        y=0,
        icon='?',
        color=(255, 255, 255),
        name='<Unnamed>',
        ai_cls,
        fighter,
        inventory,
    ):
        super().__init__(
            x=x,
            y=y,
            icon=icon,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

    @property
    def is_alive(self):
        ''' Returns True as long as this actor can perform actions '''
        return bool(self.ai)
