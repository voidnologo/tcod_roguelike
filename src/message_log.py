"""Message log for displaying game messages."""

from __future__ import annotations

import textwrap
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING

import color as color_module

if TYPE_CHECKING:
    from tcod.console import Console

    from game_types import ColorRGB


@dataclass(slots=True)
class Message:
    """A single message in the message log."""

    plain_text: str
    fg: ColorRGB
    count: int = 1

    @property
    def full_text(self) -> str:
        """Return the message text with count if stacked."""
        if self.count > 1:
            return f'{self.plain_text} (x{self.count})'
        return self.plain_text


class MessageLog:
    """A log of game messages with rendering capabilities."""

    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add_message(
        self,
        text: str,
        fg: ColorRGB = color_module.white,
        *,
        stack: bool = True,
    ) -> None:
        """Add a message to the log.

        Args:
            text: The message text
            fg: Text color
            stack: If True, stack with previous identical messages
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, console: Console, x: int, y: int, width: int, height: int) -> None:
        """Render the message log to the console."""
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def wrap(string: str, width: int) -> Iterator[str]:
        """Yield wrapped lines from a string."""
        for line in string.splitlines():
            yield from textwrap.wrap(line, width, expand_tabs=True)

    @classmethod
    def render_messages(
        cls,
        console: Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: list[Message],
    ) -> None:
        """Render a list of messages to the console."""
        y_offset = height - 1
        for message in reversed(messages):
            for line in reversed(list(cls.wrap(message.full_text, width))):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return
