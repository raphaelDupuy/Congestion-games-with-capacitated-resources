class resource:

    def __init__(self, players, capacity, position):
        self.players = players
        self.capacity = capacity
        self.position = position

    def getCapacity(self):
        return self.capacity
    
    def getPlayers(self):
        return self.players
    
    def getDelay(self):
        return min(self.getPlayers().size(), self.capacity)

    