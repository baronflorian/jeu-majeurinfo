from collections import deque
import attaque
from parcours import parcour
import valeur
from joueur import Joueur, Ordi



    

def menu_de_debut():
    
    print("Bienvenue dans le jeu de combat !")
    print("Vous allez affronter le dark magician.")
    print("Vous pourrez choisir parmis les éléments suivants")
    print(valeur.regle)
    print(valeur.menu)
print(menu_de_debut())




def tour_de_jeu(attaquant, defenseur):
   
    print(f"\nC'est au tour de {attaquant.nom} !")
    if not attaquant.est_vivant():
        print(f"{attaquant.nom} est mort.")
        return False
    if not defenseur.est_vivant():
        print(f"{defenseur.nom} est mort.")
        return False
    tour=1
    degat1,carte1=attaque.attaquer(attaquant,defenseur)
    if degat1>=defenseur.vie:
        print(f"{defenseur.nom} est mort.")
        return False
    tour=2
    degat2,carte2=attaque.attaquer(defenseur,attaquant)

    attaquant.lulu+=degat1
    defenseur.lulu+=degat2

    if carte2==valeur.carte_complementaire[carte1]:
        if degat1>degat2:
            degat1=degat1-degat2 +2
            degat2=0
        else:
            degat2=degat2-degat1 +2
            degat1=0
    attaquant.vie-=degat2
    defenseur.vie-=degat1
  
    



   















def main():
    menu_de_debut
    joueur = Joueur(valeur.menu_actions_disponible())
    continuer = "1"
    while continuer == "1":
        if lulu >= 20:
            parcours.bouger(lettre)
        else: 
            carte = joueur.choisir_carte()
            print("Tu joues la :",carte, "contre le dark magician")
            continuer = input("Tu veux continuer : oui tape 1 non tape 2 : ")
    exit() # car on est sorti de la boucle.

if __name__ == "__main__":
    main()