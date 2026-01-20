"""Custom exceptions for the game."""

from __future__ import annotations


class ImpossibleActionError(Exception):
    """Exception raised when an action cannot be performed."""


class QuitWithoutSaving(SystemExit):
    """Exception raised to exit the game without saving."""
