from components.ai import BaseAI, HostileEnemy
from components.healing_consumable import HealingConsumable
from components.lightening_damage_consumable import LighteningDamageConsumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    icon='@',
    color=(255, 128, 0),
    name='Player',
    ai_cls=BaseAI,
    fighter=Fighter(
        hp=30,
        defense=2,
        power=5,
    ),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    icon='o',
    color=(63, 127, 63),
    name='Orc',
    ai_cls=HostileEnemy,
    fighter=Fighter(
        hp=10,
        defense=0,
        power=3,
    ),
    inventory=Inventory(capacity=0),
)

troll = Actor(
    icon='T',
    color=(0, 127, 0),
    name='Troll',
    ai_cls=HostileEnemy,
    fighter=Fighter(
        hp=16,
        defense=1,
        power=4,
    ),
    inventory=Inventory(capacity=0),
)

health_potion = Item(
    icon='!',
    color=(128, 0, 128),
    name='Health Potion',
    consumable=HealingConsumable(amount=4),
)

lightening_scroll = Item(
    icon='~',
    color=(255, 165, 83),
    name='Lightening Scroll',
    consumable=LighteningDamageConsumable(damage=20, maximum_range=5),
)
