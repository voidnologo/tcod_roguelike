import numpy as np
import tcod as libtcod

from actions import Action, MeleeAction, MovementAction, WaitAction


class BaseAI(Action):
    entity = None

    def perform(self):
        raise NotImplementedError()

    def get_path_to(self, dest_x, dest_y):
        cost = np.array(self.entity.gamemap.tiles['walkable'], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # add to the cost of the blocked position
                # a lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths
                # in order to surround the player
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder
        graph = libtcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = libtcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))

        # Compute the path to the destination and remove the starting point
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert the path format
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self):
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity,
                dest_x - self.entity.x,
                dest_y - self.entity.y,
            ).perform()
        return WaitAction(self.entity).perform()
