"""Item action for using items."""

from __future__ import annotations

from typing import TYPE_CHECKING

from actions.base_action import Action

if TYPE_CHECKING:
    from entity.actor import Actor
    from entity.item import Item
    from game_types import Position


class ItemAction(Action):
    """An action for using an item, optionally at a target location."""

    def __init__(
        self,
        entity: Actor,
        item: Item,
        target_xy: Position | None = None,
    ) -> None:
        super().__init__(entity)
        self.item = item
        self.target_xy: Position = target_xy if target_xy else (entity.x, entity.y)

    @property
    def target_actor(self) -> Actor | None:
        """Return the actor at the target location."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Activate the item's consumable ability."""
        self.item.consumable.activate(self)
