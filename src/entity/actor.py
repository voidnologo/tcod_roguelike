"""Actor entity class for creatures that can take actions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from entity.base_entity import Entity
from render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai.base_ai import BaseAI
    from components.fighter import Fighter
    from components.inventory import Inventory
    from game_types import ColorRGB


class Actor(Entity):
    """A living entity that can perform actions."""

    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        icon: str = '?',
        color: ColorRGB = (255, 255, 255),
        name: str = '<Unnamed>',
        ai_cls: type[BaseAI],
        fighter: Fighter,
        inventory: Inventory,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            icon=icon,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: BaseAI | None = ai_cls(self)
        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
