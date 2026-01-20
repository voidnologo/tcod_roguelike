"""Entity factory templates and instances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from components.ai import BaseAI, HostileEnemy
from components.confusion_consumable import ConfusionConsumable
from components.fighter import Fighter
from components.fireball_damage_consumable import FireballDamageConsumable
from components.healing_consumable import HealingConsumable
from components.inventory import Inventory
from components.lightning_damage_consumable import LightningDamageConsumable
from entity import Actor, Item

if TYPE_CHECKING:
    from components.consumable import Consumable
    from game_types import ColorRGB


@dataclass(frozen=True, slots=True)
class ActorTemplate:
    """Template for creating actor entities."""

    icon: str
    color: ColorRGB
    name: str
    ai_cls: type[BaseAI]
    hp: int
    defense: int
    power: int
    inventory_capacity: int = 0

    def create(self) -> Actor:
        """Create an Actor from this template."""
        return Actor(
            icon=self.icon,
            color=self.color,
            name=self.name,
            ai_cls=self.ai_cls,
            fighter=Fighter(hp=self.hp, defense=self.defense, power=self.power),
            inventory=Inventory(capacity=self.inventory_capacity),
        )


@dataclass(frozen=True, slots=True)
class ItemTemplate:
    """Template for creating item entities."""

    icon: str
    color: ColorRGB
    name: str
    consumable: Consumable

    def create(self) -> Item:
        """Create an Item from this template."""
        return Item(
            icon=self.icon,
            color=self.color,
            name=self.name,
            consumable=self.consumable,
        )


# Actor templates
PLAYER_TEMPLATE = ActorTemplate(
    icon='@',
    color=(255, 128, 0),
    name='Player',
    ai_cls=BaseAI,
    hp=30,
    defense=2,
    power=5,
    inventory_capacity=26,
)

ORC_TEMPLATE = ActorTemplate(
    icon='o',
    color=(63, 127, 63),
    name='Orc',
    ai_cls=HostileEnemy,
    hp=10,
    defense=0,
    power=3,
)

TROLL_TEMPLATE = ActorTemplate(
    icon='T',
    color=(0, 127, 0),
    name='Troll',
    ai_cls=HostileEnemy,
    hp=16,
    defense=1,
    power=4,
)

# Actor instances (for spawning)
player = Actor(
    icon='@',
    color=(255, 128, 0),
    name='Player',
    ai_cls=BaseAI,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    icon='o',
    color=(63, 127, 63),
    name='Orc',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)

troll = Actor(
    icon='T',
    color=(0, 127, 0),
    name='Troll',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)

# Item instances
health_potion = Item(
    icon='!',
    color=(128, 0, 128),
    name='Health Potion',
    consumable=HealingConsumable(amount=4),
)

lightning_scroll = Item(
    icon='~',
    color=(255, 165, 83),
    name='Lightning Scroll',
    consumable=LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    icon='~',
    color=(207, 63, 255),
    name='Confusion Scroll',
    consumable=ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    icon='~',
    color=(255, 0, 0),
    name='Fireball Scroll',
    consumable=FireballDamageConsumable(damage=12, radius=3),
)
