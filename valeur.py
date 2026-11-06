from collections import deque


def menu_actions_disponible():
    action = deque(['Feu','Glace','Eclair','Lave','Eau','Terre','Magie','Temps']) 
    return action
lulu_joueur = 10
lulu_IA = 10
regle= """Régles du jeux : Le but est de tuer le dark magician; chaque élément donne des dégats. \n " \
    "Si le dark magician lance une action complémentaire à notre attaque, \n
    un seul prend les dégats de pv : la difference des dégats des 2attaques, \n" \
    " si pendant deux attaques de suite l'utilisateur ne recoit pas de degats, \n" \
    " c'est a dire qu'il a pu obtenir deux attaques complémentaire d'affilé \n" \
    "et que ses deux attaques complémentaires étaient de points de dégats plus élevés que le dark magician \n" \
    "alors on gagne 6 points de vie en plus /n" \
    "on peut sélectionner à chaque tour une carte parmis quatre cartes parmis les 8 du jeux "
    "(on ne pourra donc pas réutiliser deux fois d'affilé la même carte)\n" \
    "quand l'utilisateur/l'ia aura 20 lulu, le user / l'ia pourra se deplacer," \
    " le joueur dapres lancera une attaus sans toucher l'adversaire." \
    "le joueur gagne quand il arrive a la postition de l'autre joueur\n" \
    "toute attaque est comptabilisé si et sueleement le joueur précedent n'a pas bougé \n
    si le joueur A ou le joueur B arrive à la position du joueur B ou A alors le joueur A a gagne."""

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


degat_elements={"Feu": 10, "Eau": 12, "Glace": 8, "Lave": 12, "Foudre": 14, "Terre": 16, "Magie": 20, "Temps": 18}