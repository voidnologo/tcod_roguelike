"""Item entity class for objects that can be picked up and used."""

from __future__ import annotations

from typing import TYPE_CHECKING

from entity.base_entity import Entity
from render_order import RenderOrder

if TYPE_CHECKING:
    from components.consumable import Consumable
    from game_types import ColorRGB


class Item(Entity):
    """An entity that can be picked up and used."""

    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        icon: str = '?',
        color: ColorRGB = (255, 255, 255),
        name: str = '<Unnamed>',
        consumable: Consumable,
    ) -> None:
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
