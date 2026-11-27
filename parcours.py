import heapq

import valeur


def trouver_position(plateau, lettre):     #on parcour tout le labyrinthe afin de trouver la position de l'element recherché(ici soit la position du joueur soit de l'ordinateur soit de la sortie)
    for y, ligne in enumerate(plateau):
        for x, case in enumerate(ligne):
            if case == lettre:
                return x, y
    return None


def position_valide(plateau, x, y):    # on verifie que la position rechercher appartient bien au labyrinthe et qu'elle ne se trouve pas sur un mur 
    return (
        0 <= y < len(plateau)
        and 0 <= x < len(plateau[y])
        and plateau[y][x] != "#"
    )


def voisins(plateau, x, y):
    #Renvoie les cases qui sont accessibles depuis notre position.
    cases = []
    for dx, dy in valeur.DIRECTIONS.values():
        nx, ny = x + dx, y + dy
        if position_valide(plateau, nx, ny):
            cases.append((nx, ny))
    return cases


def construire_graphe(plateau):
    """Transforme le plateau en graphe : chaque clé correspond a une case et ses valeurs sont la liste des cases voisines ou on peut aller.
    Le graphe sert notament a trouver le plus court chemin entre 2 destination dans A_star"""
    graphe = {}
    for y, ligne in enumerate(plateau):
        for x, case in enumerate(ligne):
            if case != "#":
                graphe[(x, y)] = voisins(plateau, x, y)
    return graphe


def distance_manhattan(a, b):
    """Heuristique : nombre de cases à parcourir horizontalement + verticalement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(graphe, depart, arrivee):
    """Renvoie le plus court chemin entre depart et arrivee sous forme de liste de positions."""
    # file de priorité : (coût estimé, coût réel, position)
    file = [(distance_manhattan(depart, arrivee), 0, depart)]
    couts = {depart: 0}   # meilleur coût connu pour chaque case
    parents = {}          # case précédente, pour reconstruire le chemin

    while file:
        _, cout, position = heapq.heappop(file)

        if position == arrivee:
            # On remonte les parents pour reconstruire le chemin
            chemin = [position]
            while position in parents:
                position = parents[position]
                chemin.append(position)
            chemin.reverse()
            return chemin

        # Si on a déjà trouvé mieux pour cette case, on ignore
        if cout > couts.get(position, float("inf")):
            continue

        for voisin in graphe.get(position, []):
            nouveau_cout = cout + 1
            if nouveau_cout < couts.get(voisin, float("inf")):
                couts[voisin] = nouveau_cout
                parents[voisin] = position
                priorite = nouveau_cout + distance_manhattan(voisin, arrivee)
                heapq.heappush(file, (priorite, nouveau_cout, voisin))

    return []   # aucun chemin trouvé


def deplacer_vers(plateau, lettre, nx, ny):
    """Déplace la `lettre` correspondant a la position du joueur qui se deplace.
    Renvoie le contenu initial de la case, ou None si le déplacement est bloqué."""
    x, y = trouver_position(plateau, lettre)     
    if not position_valide(plateau, nx, ny):
        return None
                                                                        #on verifie que la position actuelle puis que 
    destination = plateau[ny][nx]                                       #la position sur laquelle on veux se deplacer soit accessible
    cases_accessibles = (" ", "|") if lettre == "J" else (" ", "J")
    if destination not in cases_accessibles:
        return None

    plateau[y][x] = " "
    plateau[ny][nx] = lettre    
    return destination


def bouger(plateau, lettre, direction):
    """renvoie la position a laquelle le joueur a choisit de se déplacer (z/s/q/d)."""
    x, y = trouver_position(plateau, lettre)
    dx, dy = valeur.DIRECTIONS[direction]
    return deplacer_vers(plateau, lettre, x + dx, y + dy)

def trouver_case_avant_sortie(plateau,lettre):
        for y, ligne in enumerate(plateau):
            for x, case in enumerate(ligne):
                if case == lettre:
                    voisin=voisins(plateau,x,y)
                    return voisin
        return None