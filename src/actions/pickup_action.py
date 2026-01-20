"""Pickup action for collecting items."""

from __future__ import annotations

import exceptions
from actions.base_action import Action


class PickupAction(Action):
    """An action that picks up an item at the entity's location."""

    def perform(self) -> None:
        """Pick up the item at the entity's location."""
        actor_x, actor_y = self.entity.x, self.entity.y
        inventory = self.entity.inventory

        item = next(
            (i for i in self.engine.game_map.items if i.x == actor_x and i.y == actor_y),
            None,
        )

        if item is None:
            raise exceptions.ImpossibleActionError('There is nothing here to pick up.')

        if inventory.full:
            raise exceptions.ImpossibleActionError('Your inventory is full.')

        self.engine.game_map.entities.discard(item)
        item.parent = self.entity.inventory
        inventory.items.append(item)

        self.engine.message_log.add_message(f'You picked up the {item.name}.')
