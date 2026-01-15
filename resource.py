class Resource:
    def __init__(self, name, capacity, position, delay):
        self.name = name
        self.capacity = capacity
        self.position = position    # dict {player_id: rank}
        self.delay = delay          # fonction dr(k)

    def getCapacity(self):
        return self.capacity
