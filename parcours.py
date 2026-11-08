import heapq

import valeur


def trouver_position(plateau, lettre):
    for y, ligne in enumerate(plateau):
        for x, case in enumerate(ligne):
            if case == lettre:
                return x, y
    return None


def position_valide(plateau, x, y):
    return (
        0 <= y < len(plateau)
        and 0 <= x < len(plateau[y])
        and plateau[y][x] != "#"
    )


def voisins(plateau, x, y):
    """Renvoie les cases marchables autour de (x, y)."""
    cases = []
    for dx, dy in valeur.DIRECTIONS.values():
        nx, ny = x + dx, y + dy
        if position_valide(plateau, nx, ny):
            cases.append((nx, ny))
    return cases


def construire_graphe(plateau):
    """Transforme le plateau en graphe : case -> liste des cases voisines ou on peut aller. (pas de murs)"""
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
    """Renvoie le plus court chemin entre depart et arrivee (liste de positions)."""
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
    """Déplace `lettre` sur la case (nx, ny).
    Renvoie None si impossible, True s'il écrase l'autre, False sinon."""
    x, y = trouver_position(plateau, lettre)
    if not position_valide(plateau, nx, ny):
        return None

    ecrasement = plateau[ny][nx] != " "      # True s'il écrase l'autre
                                            # False si il va sur une case vide
    plateau[y][x] = " "                      # on vide la case où il était
    plateau[ny][nx] = lettre                 # on écrit le joueur dans sa nouvelle case
    return ecrasement


def bouger(plateau, lettre, direction):
    """Déplace le joueur dans une direction (z/s/q/d)."""
    x, y = trouver_position(plateau, lettre)
    dx, dy = valeur.DIRECTIONS[direction]
    return deplacer_vers(plateau, lettre, x + dx, y + dy)
