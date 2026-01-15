class Player:
    def __init__(self, id, strat=None):
        self.id = id
        self.strat = strat if strat is not None else set()

    def getStrat(self):
        return self.strat
    
    def setStrat(self, strat):
        self.strat = strat

    def getId(self):
        return self.id
