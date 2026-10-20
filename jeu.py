from joueur_ordi import JoueurOrdi
from joueur import Joueur
from collections import deque
def menu_de_debut():
    
    print("Bienvenue dans le jeu de combat !")
    print("Vous allez affronter le dark magician.")
    print("Vous pourrez choisir parmis les éléments suivants")
    print("Régles du jeux : Le but est de tuer le dark magician; chaque éléments donne des dégats. \n " \
    "Si on lance avec le dark magician une action complémentaire un seul prends les dégats de points : la differences de deux, \n" \
    " si pendant deux attaques de suite l'utilisateur ne recoit pas de degats, \n" \
    " c'est a dire qu'il a pu obtenir deux attaques complémentaire d'affilé \n" \
    "et que ses deux attauses complémentaire étaient de points de dégats plus élevés que le dark magician \n" \
    "alors on gagne 6 points de vie un plus /n" \
    "on peut slectionner à chaque tour un carte parmis quatre cartes parmis les 8 du jeux "
    "(on ne pourra donc pas réutiliser deux fois d'affilé la même carte)")
    print("""| Élément | Points de dégâts |
|---------|------------------|
| Feu     | 10               |
| Eau     | 12               |
| Glace   | 8                |
| Lave    | 12               |
| Foudre  | 14               |
| Terre   | 16               |
| Magie   | 20               |
| Temps   | 18               |""")
print(menu_de_debut())
def menu_actions_disponible():
    action = deque()
    action.append("Feu")
    action.append("Glace")
    action.append("Eclair") 
    action.append("Lave")
    action.append("Eau")
    action.append("Terre")
    action.append("Magie")
    action.append("Temps")
    return action
def main():
    menu_de_debut
    joueur = Joueur(menu_actions_disponible())
    continuer = "1"
    while continuer == "1":
        carte = joueur.choisir_carte()
        print("Tu joues la :",carte, "contre le dark magician")
        continuer = input("Tu veux continuer : oui tape 1 non tape 2 : ")
    "si le user tape deux il faudra arrete le prog"

if __name__ == "__main__":
    main()