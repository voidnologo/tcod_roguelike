from components.base_component import BaseComponent
from input_handlers import GameOverEventHandler
from render_order import RenderOrder


class Fighter(BaseComponent):
    entity = None

    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self):
        if self.engine.player is self.entity:
            death_message = 'You Died!'
            self.engine.event_handler = GameOverEventHandler(self.engine)
        else:
            death_message = f'{self.entity.name} is dead!'

        self.entity.icon = '%'
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f'remains of {self.entity.name}'
        self.entity.render_order = RenderOrder.CORPSE

        print(death_message)
