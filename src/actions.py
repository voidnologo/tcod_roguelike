class Action:
    pass


class EscapeAction(Action):
    def __init__(self):
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, dx, dy):
        super().__init__()

        self.dx = dx
        self.dy = dy
