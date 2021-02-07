from input_handlers.select_index_handler import SelectIndexHandler


class LookHandler(SelectIndexHandler):
    """
    Lets the player look around using the keyboard
    """

    def on_index_selected(self, x, y):
        from input_handlers.main_game_event_handler import MainGameEventHandler

        return MainGameEventHandler(self.engine)
