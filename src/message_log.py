import textwrap

import color


class Message:
    def __init__(self, text, fg):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self):
        if self.count > 1:
            return f'{self.plain_text} (x{self.count})'
        return self.plain_text


class MessageLog:
    def __init__(self):
        self.messages = []

    def add_message(self, text, fg=color.white, *, stack=True):
        """
        Add messages to log
        `text` is the message text
        `fg` is text color
        If `stack` is true, then the message can stack with previous message of the same text.
        """
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(self, console, x, y, width, height):
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(console, x, y, width, height, messages):
        y_offset = height - 1
        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # no more space
