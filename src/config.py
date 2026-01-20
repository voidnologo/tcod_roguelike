"""Game configuration dataclass."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameConfig:
    """Immutable game configuration settings."""

    screen_width: int = 80
    screen_height: int = 60
    map_width: int = 80
    map_height: int = 50

    room_max_size: int = 10
    room_min_size: int = 6
    max_rooms: int = 30

    max_monsters_per_room: int = 2
    max_items_per_room: int = 2

    fov_radius: int = 8

    message_box_x: int = 21
    message_box_y: int = 51
    message_box_width: int = 40
    message_box_height: int = 9

    health_bar_width: int = 20


DEFAULT_CONFIG = GameConfig()
