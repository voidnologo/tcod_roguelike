from input_handlers.select_index_handler import SelectIndexHandler


class SingleRangedAttackHandler(SelectIndexHandler):
    def __init__(self, engine, callback):
        super().__init__(engine)
        self.callback = callback

    def on_index_selected(self, x, y):
        return self.callback((x, y))
