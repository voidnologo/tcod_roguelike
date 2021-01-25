import color
from input_handlers.select_index_handler import SelectIndexHandler


class AreaRangedAttackHandler(SelectIndexHandler):
    """
    Handles targeting an area within a given radius.
    All entities in area will be affected.
    """

    def __init__(self, engine, radius, callback):
        super().__init__(engine)
        self.radius = radius
        self.callback = callback

    def on_render(self, console):
        super().on_render(console)
        x, y = self.engine.mouse_location

        # Draw a rectangle around the target area
        console.draw_frame(
            x=x - self.radius - 1,
            y=y - self.radius - 1,
            width=self.radius ** 2,
            height=self.radius ** 2,
            fg=color.red,
            clear=False,
        )

    def on_index_selected(self, x, y):
        return self.callback((x, y))
