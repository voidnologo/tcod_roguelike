import tcod as libtcod

import color
from input_handlers.ask_user_event_handler import AskUserEventHandler


class InventoryEventHandler(AskUserEventHandler):
    """
    This event handler lets the user select an item.
    Subclass handles activity.
    """

    TITLE = '<missing title>'

    def on_render(self, console):
        """
        Render an inventory menu, which displays the items in an inventory with select menu.
        Will move to a different position based on player location so they remain visible.
        """
        super().on_render(console)
        number_of_items_in_inventory = len(self.engine.player.inventory.items)

        height = max(3, number_of_items_in_inventory + 2)
        x = 40 if self.engine.player.x <= 30 else 0
        y = 0

        width = len(self.TITLE) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=height,
            title=self.TITLE,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        if number_of_items_in_inventory > 0:
            for i, item in enumerate(self.engine.player.inventory.items):
                item_key = chr(ord('a') + i)
                console.print(x + 1, y + i + 1, f'({item_key}) {item.name})')
        else:
            console.print(x + 1, y + 1, '(Empty)')

    def ev_keydown(self, event):
        player = self.engine.player
        key = event.sym
        index = key - libtcod.event.K_a

        if 0 <= index <= 26:
            try:
                selected_item = player.inventory.items[index]
            except IndexError:
                self.engine.message_log.add_message('Invalid entry.', color.invalid)
                return None
            return self.on_item_selected(selected_item)
        return super().ev_keydown(event)

    def on_item_selected(self, item):
        raise NotImplementedError()
