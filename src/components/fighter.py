import color
from components.base_component import BaseComponent
from render_order import RenderOrder


class Fighter(BaseComponent):
    parent = None

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
        if self._hp == 0 and self.parent.ai:
            self.die()

    def die(self):
        if self.engine.player is self.parent:
            death_message = 'You Died!'
            death_message_color = color.player_die
        else:
            death_message = f'{self.parent.name} is dead!'
            death_message_color = color.enemy_die

        self.parent.icon = '%'
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f'remains of {self.parent.name}'
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

    def heal(self, amount):
        if self.hp == self.max_hp:
            return 0

        new_hp_value = min(self.max_hp, self.hp + amount)
        amount_recovered = new_hp_value - self.hp
        self.hp = new_hp_value
        return amount_recovered

    def take_damage(self, amount):
        self.hp -= amount
