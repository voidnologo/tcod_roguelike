from actions.base_action import Action


class EscapeAction(Action):
    def perform(self):
        raise SystemExit()
