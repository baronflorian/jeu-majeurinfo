from collections import deque

# --- Réglages du jeu ---
VIE_DEPART = 80
VIE_DEPART_ORDI_DIFFICILE = 95
LULU_DEPART = 0
LULU_POUR_BOUGER = 22
LULU_POUR_SOIGNER = 10
PV_SOIGNES = 14

# --- Plateaux possibles ---
# M = Dark Magician, J = joueur, # = mur, | = sortie, espace = case libre.
# Chaque ligne doit avoir la même longueur. La sortie est une ouverture dans un mur extérieur.
plateaux = {
    "petit": [
        "#####",
        "#J  #",
        "# # #",
        "#  M|",
        "#####",
    ],
    "moyen": [
        "#########",
        "#J      #",
        "# ##### #",
        "#   #   #",
        "### # ###",
        "#   #   #",
        "# ##### #",
        "#      M|",
        "#########",
    ],
    "grand": [
        "###########",
        "#J        #",
        "#### ### ##",
        "#      #  #",
        "# #### ## #",
        "#    #    #",
        "#### # ## #",
        "#         #",
        "# ###### ##",
        "#        M|",
        "###########",
    ],
}

# Pour changer de plateau, remplace "petit" par "moyen" ou "grand".
def changer_plateau(nom):
    global plateau
    plateau = [list(ligne) for ligne in plateaux[nom]]


# z = haut, s = bas, q = gauche, d = droite 
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

difficultes = {1: 0.85, 2: 1, 3: 1.15}

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


# Textes affichés
regle = (
    "Tu gagnes si tu bats le Dark Magician avec tes attaques ou si tu atteins la sortie | du labyrinthe.\n"
    "- Tu perds si le Dark Magician arrive sur ta case ou si ses attaques te font perdre tous tes PV.\n"
    "- Sur le plateau, J te représente et M représente le Dark Magician. Sa case bloque ton passage.\n"
    "- Chaque carte inflige les dégâts indiqués ci-dessous.\n"
    "- Pour jouer Foudre ou Terre, tu dépenses 2 lulu. Pour jouer Magie ou Temps, tu dépenses 4 lulu.\n"
    "- Tes autres cartes sont gratuites.\n"
    "- Si aucune carte en main n'est jouable, tu passes ton tour et une nouvelle carte entre dans ta main à la fin du tour.\n"
    "- Si deux cartes complémentaires ont des puissances différentes, celui qui a joué la plus faible subit la différence de dégâts plus 2.\n"
    "- Si elles sont de même puissance, les attaques s'annulent.\n"
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




distance_limite = {1: -float("inf"), 2: 4, 3: 6}    #le petit labyrinthe est trop petit pour aplliquer l'heuristique
distance_poursuite_limite={1: float("inf"),2:8,3:11}
