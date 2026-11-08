from collections import deque

# --- Réglages du jeu ---
VIE_DEPART = 30
LULU_DEPART = 0
LULU_POUR_BOUGER = 20

# --- Plateaux possibles ---
# A = Dark Magician, B = joueur, # = mur, espace = case libre.
# Chaque ligne doit avoir la même longueur et le plateau doit être entouré de murs.
plateaux = {
    "petit": [
        "#####",
        "#A  #",
        "# # #",
        "#  B#",
        "#####",
    ],
    "labyrinthe": [
        "#########",
        "#A      #",
        "# ##### #",
        "#   #   #",
        "### # ###",
        "#   #   #",
        "# ##### #",
        "#      B#",
        "#########",
    ],
    "piliers": [
        "###########",
        "#A        #",
        "# ## ### ##",
        "#         #",
        "# ## # ## #",
        "#    #    #",
        "# ## # ## #",
        "#         #",
        "# ## ### ##",
        "#        B#",
        "###########",
    ],
}

# Pour changer de plateau, remplace "petit" par "labyrinthe" ou "piliers".
plateau = [list(ligne) for ligne in plateaux["petit"]]

# z = haut, s = bas, q = gauche, d = droite (comme dans minecraft :) )
DIRECTIONS = {
    "z": (0, -1),
    "s": (0, 1),
    "q": (-1, 0),
    "d": (1, 0),
}


def menu_actions_disponible():
    return deque(['Feu', 'Glace', 'Foudre', 'Lave', 'Eau', 'Terre', 'Magie', 'Temps']) # file


# --- Les cartes ---
degat_elements = {
    "Feu": 10,
    "Eau": 12,
    "Glace": 8,
    "Lave": 12,
    "Foudre": 14,
    "Terre": 16,
    "Magie": 20,
    "Temps": 18,
}

# Chaque carte a une seule complémentaire
carte_complementaire = {
    "Feu": "Eau",
    "Eau": "Feu",
    "Glace": "Lave",
    "Lave": "Glace",
    "Foudre": "Terre",
    "Terre": "Foudre",
    "Magie": "Temps",
    "Temps": "Magie",
}


# --- Textes affichés ---
regle = """But : tuer le Dark Magician.
- Chaque carte inflige les dégâts indiqués ci-dessous.
- Si les deux cartes sont complémentaires, seule la plus faible subit la différence.
- Une attaque rapporte des lulu (autant de lulu gagnés que de dégats infligés).
À 20 lulu, tu peux te déplacer (le déplacement coûte 20 lulu).
- Après un déplacement, l'attaque suivante de l'adversaire ne te fait aucun dégât. 
(l'attaque est esquivée)
- Tu gagnes si le Dark Magician n'a plus de PV, ou si tu arrives sur sa case."""

menu = """| Élément | Points de dégâts |
|---------|------------------|
| Feu     | 10               |
| Eau     | 12               |
| Glace   | 8                |
| Lave    | 12               |
| Foudre  | 14               |
| Terre   | 16               |
| Magie   | 20               |
| Temps   | 18               |"""
