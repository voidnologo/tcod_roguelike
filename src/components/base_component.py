class BaseComponent:
    parent = None

    @property
    def engine(self):
        return self.gamemap.engine

    @property
    def gamemap(self):
        return self.parent.gamemap
