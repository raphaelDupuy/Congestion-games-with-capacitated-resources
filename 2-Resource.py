from player import Player
from resource import Resource

INF = 10**9

def users_of(res, players):
    """Retourne la liste des joueurs utilisant la ressource res"""
    return [p for p in players if res in p.getStrat()]

def isAccomodated(player, res, players):
    """Vérifie si un joueur est accommodé sur une ressource"""
    users = users_of(res, players)
    users.sort(key=lambda p: res.position[p.getId()])
    return player in users[:res.capacity]

def getPlayerDelay(player, res, players):
    """Calcule le délai d'un joueur sur une ressource"""
    if isAccomodated(player, res, players):
        k = min(len(users_of(res, players)), res.capacity)
        return res.delay(k)
    return INF

def getPlayerCost(player, players):
    """Calcule le coût total d'un joueur"""
    cost = 0
    for res in player.getStrat():
        cost += getPlayerDelay(player, res, players)
    return cost


# =========================
# ALGORITHME 1 (2 RESSOURCES) - VERSION CORRIGÉE
# =========================

def algo_two_resources(players, r, s):
    """
    Implémentation fidèle de l'Algorithme 1 du papier
    "Congestion games with capacitated resources"
    """
    
    # Étape 1 (ligne 2): Initialiser tous les joueurs sur r
    for p in players:
        p.setStrat({r})
    
    # Étape 2 (ligne 3): Construire N̂ (joueurs flexibles)
    # N̂ contient les joueurs dont l'espace de stratégies (réduit) est {{r}, {s}}
    # Pour simplifier, on considère tous les joueurs qui ont accès aux deux ressources
    N_hat = []
    
    for p in players:
        # Vérifier si le joueur peut potentiellement utiliser les deux ressources
        # Un joueur est flexible s'il n'est pas forcé à une seule ressource
        p.setStrat({r})
        cost_r = getPlayerCost(p, players)
        p.setStrat({s})
        cost_s = getPlayerCost(p, players)
        p.setStrat({r})  # Remettre sur r
        
        # Si au moins une des deux ressources est accessible (coût fini possible)
        # Note: dans le papier, cela correspond aux joueurs avec stratégies {{r}, {s}}
        N_hat.append(p)
    
    # Trier N̂ par ordre de priorité sur s (ligne 3)
    N_hat.sort(key=lambda p: s.position[p.getId()])
    
    # Étape 3: Identifier N̂∞ et N̂f (ligne 4)
    # N̂∞ = joueurs de N̂ avec coût infini
    # N̂f = joueurs de N̂ avec coût fini
    def get_N_infinity():
        return [p for p in N_hat if getPlayerCost(p, players) >= INF]
    
    def get_N_finite():
        return [p for p in N_hat if getPlayerCost(p, players) < INF]
    
    # PREMIÈRE BOUCLE (lignes 5-7): Éliminer les coûts infinis
    N_infinity = get_N_infinity()
    
    for i in N_infinity:
        # Ligne 6: Si i ∈ N̂∞ et ci(s, σ−i) < ci(σ) alors σi ← s
        old_cost = getPlayerCost(i, players)  # Coût actuel sur r (= ∞)
        i.setStrat({s})
        new_cost = getPlayerCost(i, players)  # Coût si on va sur s
        
        # Dans le papier: "if ci(s, σ−i) < ci(σ) then σi ← s"
        if new_cost < old_cost:
            # Rester sur s (amélioration stricte)
            pass
        else:
            # Pas mieux sur s, retour sur r
            i.setStrat({r})
    
    # DEUXIÈME BOUCLE (lignes 8-15): Optimiser les coûts finis
    # Recalculer N̂f après la première boucle
    N_finite = get_N_finite()
    
    for i in N_finite:
        current_res = list(i.getStrat())[0]  # Ressource actuelle
        
        # Ne tester que si le joueur est actuellement sur r
        # Car l'algorithme cherche à déplacer de r vers s
        if current_res != r:
            continue
        
        # Ligne 9: Si i ∈ N̂f et ci(s, σ−i) < ci(σ)
        old_cost = getPlayerCost(i, players)
        i.setStrat({s})
        new_cost = getPlayerCost(i, players)
        
        if new_cost < old_cost:
            # Ligne 10: σi ← s
            # Le joueur i se déplace vers s
            
            # Ligne 11-13: Gérer les joueurs déplacés
            users = users_of(s, players)
            users.sort(key=lambda q: s.position[q.getId()])
            
            if len(users) > s.capacity:
                # Identifier les joueurs déplacés
                displaced = users[s.capacity:]
                
                for j in displaced:
                    # Ligne 12: Si j ∈ N̂
                    if j in N_hat:
                        # Ligne 13: σj ← r
                        j.setStrat({r})
        else:
            # Ligne 14: Le mouvement n'est pas profitable, annuler
            i.setStrat({r})


# =========================
# VÉRIFICATION D'ÉQUILIBRE DE NASH
# =========================

def is_nash_equilibrium(players, resources):
    """Vérifie si le profil actuel est un équilibre de Nash"""
    for p in players:
        current_cost = getPlayerCost(p, players)
        current_strat = p.getStrat()
        
        # Tester toutes les déviations possibles
        for res in resources:
            if res not in current_strat:
                p.setStrat({res})
                new_cost = getPlayerCost(p, players)
                
                if new_cost < current_cost:
                    # Une déviation profitable existe
                    p.setStrat(current_strat)
                    return False
                
                p.setStrat(current_strat)
    
    return True


# =========================
# EXEMPLE : JEU 5 JOUEURS / 2 RESSOURCES
# =========================

if __name__ == "__main__":
    N = [Player(i) for i in range(5)]
    
    # priorités sur les ressources
    pos_r = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    pos_s = {0: 4, 1: 0, 2: 1, 3: 2, 4: 3}
    
    # fonctions de délai
    def dr(k):
        return k
    
    def ds(k):
        return 2 + k
    
    # ressources
    r = Resource("r", capacity=3, position=pos_r, delay=dr)
    s = Resource("s", capacity=2, position=pos_s, delay=ds)
    
    print("=== INITIALISATION ===")
    print("Ressource r: capacité={}, délai=d(k)=k".format(r.capacity))
    print("Ressource s: capacité={}, délai=d(k)=2+k".format(s.capacity))
    print("\nPriorités sur r:", pos_r)
    print("Priorités sur s:", pos_s)
    print()
    
    algo_two_resources(N, r, s)
    
    print("=== ÉQUILIBRE DE NASH (5 joueurs, 2 ressources) ===")
    for p in N:
        res_names = [res.name for res in p.getStrat()]
        cost = getPlayerCost(p, N)
        accommodated = all(isAccomodated(p, res, N) for res in p.getStrat())
        
        print(f"Joueur {p.getId()}: stratégie={res_names}, "
              f"coût={cost if cost < INF else '∞'}, "
              f"accommodé={'✓' if accommodated else '✗'}")
    
    print("\n=== VÉRIFICATION ===")
    is_nash = is_nash_equilibrium(N, [r, s])
    print(f"Est un équilibre de Nash: {'OUI ✓' if is_nash else 'NON ✗'}")
    
    print("\n=== DISTRIBUTION SUR LES RESSOURCES ===")
    users_r = users_of(r, N)
    users_s = users_of(s, N)
    
    print(f"Ressource r ({len(users_r)} joueurs): {[p.getId() for p in users_r]}")
    if users_r:
        print(f"  Délai: {r.delay(min(len(users_r), r.capacity))}")
    
    print(f"Ressource s ({len(users_s)} joueurs): {[p.getId() for p in users_s]}")
    if users_s:
        print(f"  Délai: {s.delay(min(len(users_s), s.capacity))}")