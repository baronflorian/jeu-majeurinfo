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


def bouger(plateau, lettre, direction):
    """Déplace le joueur. Renvoie None si impossible, True s'il écrase l'autre, False sinon."""
    x, y = trouver_position(plateau, lettre)
    dx, dy = valeur.DIRECTIONS[direction]
    nx, ny = x + dx, y + dy

    if not position_valide(plateau, nx, ny):  # le deplacement est impossible
        return None

    ecrasement = plateau[ny][nx] != " "      # True s'il écrase l'autre
                                            # False si il va sur une case vide
    plateau[y][x] = " "                      # on vide la case où il était
    plateau[ny][nx] = lettre                 # on écrit le joueur dans sa nouvelle case
    return ecrasement
