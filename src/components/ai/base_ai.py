import numpy as np
import tcod as libtcod

from actions import Action


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
