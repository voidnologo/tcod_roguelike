"""Render order enumeration for entities."""

from __future__ import annotations

from enum import Enum, auto


class RenderOrder(Enum):
    """Determines the order in which entities are rendered."""

    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
