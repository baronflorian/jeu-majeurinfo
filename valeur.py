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

cout_cartes = {
    "Foudre": 2,
    "Terre": 2,
    "Magie": 4,
    "Temps": 4,
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


# Textes affichés
regle = (
    "Tu gagnes si tu bats le Dark Magician avec tes attaques ou si tu atteins la sortie | du labyrinthe.\n"
    "- Tu perds si le Dark Magician arrive sur ta case ou si ses attaques te font perdre tous tes PV.\n"
    "- Sur le plateau, B te représente et A représente le Dark Magician. Sa case bloque ton passage.\n"
    "- Chaque carte inflige les dégâts indiqués ci-dessous.\n"
    "- Pour jouer Foudre ou Terre, tu dépenses 2 lulu. Pour jouer Magie ou Temps, tu dépenses 4 lulu.\n"
    "- Tes autres cartes sont gratuites.\n"
    "- Si aucune carte en main n'est jouable, tu passes ton tour et une carte gratuite entre dans ta main à la fin du tour.\n"
    "- Si les deux cartes sont complémentaires, seule la plus faible subit la différence.\n"
    "- Une attaque rapporte autant de lulu que de dégâts infligés.\n"
    "- Un déplacement coûte 22 lulu. Un soin coûte 10 lulu et rend jusqu'à 14 PV.\n"
    "- Après un déplacement, l'attaque suivante de l'adversaire ne te fait aucun dégât (l'attaque est esquivée)."
)

menu = """| Élément | Points de dégâts | Coût en lulu |
|---------|------------------|--------------|
| Feu     | 10               | 0            |
| Eau     | 12               | 0            |
| Glace   | 8                | 0            |
| Lave    | 12               | 0            |
| Foudre  | 14               | 2            |
| Terre   | 16               | 2            |
| Magie   | 20               | 4            |
| Temps   | 18               | 4            |"""
