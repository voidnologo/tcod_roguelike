import numpy as np

from entity import Actor, Item
from map_objects import tile_types


class GameMap:
    def __init__(self, engine, width, height, entities):
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)
        self.tiles = self.initialize_tiles()

        self.visible = np.full((width, height), fill_value=False, order='F')  # tiles player can currently see
        self.explored = np.full((width, height), fill_value=False, order='F')  # tiles player has seen

    @property
    def gamemap(self):
        return self

    def initialize_tiles(self):
        tiles = np.full(
            (self.width, self.height),
            fill_value=tile_types.wall,
            order='F',
        )

        tiles[30:33, 22] = tile_types.wall
        return tiles

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(  # noqa: E203
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles['light'], self.tiles['dark']],
            default=tile_types.FOW,
        )

        for entity in sorted(self.entities, key=lambda x: x.render_order.value):
            # only print entities in FOV
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.icon, fg=entity.color)

    def get_blocking_entity_at_location(self, location_x, location_y):
        for entity in self.entities:
            if all(
                (
                    entity.blocks_movement,
                    entity.x == location_x,
                    entity.y == location_y,
                )
            ):
                return entity
        return None

    @property
    def actors(self):
        yield from (entity for entity in self.entities if isinstance(entity, Actor) and entity.is_alive)

    @property
    def items(self):
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_actor_at_location(self, location_x, location_y):
        for actor in self.actors:
            if actor.x == location_x and actor.y == location_y:
                return actor
        return None
