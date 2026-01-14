
class player:

    def __init__(self, id, strat={}):
        self.id = id
        self.strat = strat

    def getStrat(self) -> set:
        return self.strat
    
    def setStrat(self, strat):
        self.strat = strat

    def getId(self):
        return self.id
