from collections import deque

# --- Réglages du jeu ---
VIE_DEPART = 80
LULU_DEPART = 0
LULU_POUR_BOUGER = 22
LULU_POUR_SOIGNER = 10
PV_SOIGNES = 14

# --- Plateaux possibles ---
# A = Dark Magician, B = joueur, # = mur, | = sortie, espace = case libre.
# Chaque ligne doit avoir la même longueur. La sortie est une ouverture dans un mur extérieur.
plateaux = {
    "petit": [
        "#####",
        "#B  #",
        "# # #",
        "#  A|",
        "#####",
    ],
    "moyen": [
        "#########",
        "#B      #",
        "# ##### #",
        "#   #   #",
        "### # ###",
        "#   #   #",
        "# ##### #",
        "#      A|",
        "#########",
    ],
    "grand": [
        "###########",
        "#B        #",
        "# ## ### ##",
        "#         #",
        "# ## # ## #",
        "#    #    #",
        "# ## # ## #",
        "#         #",
        "# ## ### ##",
        "#        A|",
        "###########",
    ],
}

# Pour changer de plateau, remplace "petit" par "labyrinthe" ou "piliers".
def changer_plateau(nom):
    global plateau
    plateau = [list(ligne) for ligne in plateaux[nom]]
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
    "Glace": "Lave",
    "Foudre": "Terre",
    "Terre": "Foudre",
    "Magie": "Temps",
    "Temps": "Magie",
}


#  Textes affichés
regle = """Tu gagnes si tu bats le Dark Magician avec tes attaques ou si tu atteins la sortie | du labyrinthe.
- Tu perds si le Dark Magician arrive sur ta case ou si ses attaques te font perdre tous tes PV.
- Sur le plateau, B te représente et A représente le Dark Magician. Sa case bloque ton passage.
- Chaque carte inflige les dégâts indiqués ci-dessous.
- Si les deux cartes sont complémentaires, seule la plus faible subit la différence.
- Une attaque rapporte des lulu (autant de lulu gagnés que de dégats infligés).
- À 22 lulu, tu peux te déplacer ou/et te soigner +14pv (se soigner coûte 12 lulu)
- Après un déplacement, l'attaque suivante de l'adversaire ne te fait aucun dégât (l'attaque est esquivée)."""

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
