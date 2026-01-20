"""Game engine for managing game state and rendering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.map import compute_fov

import exceptions
from config import DEFAULT_CONFIG
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
    from tcod.console import Console

    from config import GameConfig
    from entity.actor import Actor
    from map_objects.game_map import GameMap


class Engine:
    """Main game engine that manages game state and rendering."""

    game_map: GameMap

    def __init__(self, player: Actor, config: GameConfig = DEFAULT_CONFIG) -> None:
        self.event_handler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location = (0, 0)
        self.config = config

    def render(self, console: Console) -> None:
        """Render the game state to the console."""
        self.game_map.render(console)

        self.message_log.render(
            console=console,
            x=self.config.message_box_x,
            y=self.config.message_box_y,
            width=self.config.message_box_width,
            height=self.config.message_box_height,
        )

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            max_value=self.player.fighter.max_hp,
            total_width=self.config.health_bar_width,
        )

        render_names_at_mouse_location(
            console,
            x=self.config.message_box_x,
            y=self.config.message_box_y - 1,
            engine=self,
        )

    def update_fov(self) -> None:
        """Recompute the visible area based on the player's point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles['transparent'],
            (self.player.x, self.player.y),
            radius=self.config.fov_radius,
        )
        self.game_map.explored |= self.game_map.visible

    def handle_enemy_turns(self) -> None:
        """Process AI turns for all enemies."""
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.ImpossibleActionError:
                    pass
