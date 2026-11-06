



from collections import deque

import valeur
from joueur import Joueur, Ordi


def menu_de_debut():
    
    print("Bienvenue dans le jeu de combat !")
    print("Vous allez affronter le dark magician.")
    print("Vous pourrez choisir parmis les éléments suivants")
    print(valeur.regle)
    print(valeur.menu)
print(menu_de_debut())

def main():
    menu_de_debut
    joueur = Joueur(valeur.menu_actions_disponible())
    continuer = "1"
    while continuer == "1":
        carte = joueur.choisir_carte()
        print("Tu joues la :",carte, "contre le dark magician")
        continuer = input("Tu veux continuer : oui tape 1 non tape 2 : ")
    "si le user tape deux il faudra arrete le prog"

if __name__ == "__main__":
    main()