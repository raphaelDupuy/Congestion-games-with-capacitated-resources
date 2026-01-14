import player
import resource

N = {player(i, {}) for i in range(3)}

r = resource([], capacite_r, position_r)
s = resource([], capacite_s, position_s)

R = {r, s};

E = {}

def isAccomodated(i, res):
    if not i in res.getPlayers():
        return False
    elif res.players.getIndex(i) < res.capacite:
        return True
    return False

def getPlayerDelay(i, res):
    if isAccomodated(i, res):
        return res.getDelay()
    else:
        return 10000000
    
def getPlayerCost(i):
    c = 0
    for res in R:
        c += getPlayerDelay(i, res)
    return c


for player in N:
    if player.getStrat().size() != 1 :
        player.setStrat({"r"})
        E.add(player.getId())
