"""Wait action for passing a turn."""

from __future__ import annotations

from actions.base_action import Action


class WaitAction(Action):
    """An action that does nothing, passing the entity's turn."""

    def perform(self) -> None:
        """Do nothing."""
        pass
