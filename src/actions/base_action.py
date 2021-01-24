class Action:
    def __init__(self, entity):
        self.entity = entity

    @property
    def engine(self):
        return self.entity.gamemap.engine

    def perform(self):
        """
        Perform this action with the objects needed to determine its scope.
        `self.engine` is the scope this action is being performed in.
        `self.entity` is the object performing the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()
