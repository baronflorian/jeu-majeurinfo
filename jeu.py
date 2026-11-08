import attaque
import valeur
from joueur import Joueur, Ordi
from parcours import bouger


def menu_de_debut():
    print("Bienvenue dans le jeu de combat !")
    print("Vous allez affronter le Dark Magician.\n")
    print(valeur.regle)
    print()
    print(valeur.menu)


def afficher_plateau():
    for ligne in valeur.plateau:
        print(" ".join(ligne))
    print()


def afficher_etat(joueur, ordi):
    print(f"Toi : {joueur.vie} PV | {joueur.lulu} lulu")
    print(f"Dark Magician : {ordi.vie} PV | {ordi.lulu} lulu")


def demander_action(joueur, ordi):
    while True:
        afficher_plateau()
        afficher_etat(joueur, ordi)
        print("a = attaquer   d = se déplacer   q = quitter")
        choix = input("Ton choix : ").lower()

        if choix == "a":
            return "a"
        if choix == "q":
            return "q"
        if choix == "d":
            if joueur.peut_bouger():
                return "d"
            print("\nIl te faut 20 lulu pour te déplacer.\n")
        else:
            print("\nChoix invalide.\n")


def demander_direction():
    while True:
        direction = input("Direction (z haut, s bas, q gauche, d droite) : ").lower()

        if direction not in valeur.DIRECTIONS:
            print("Direction invalide.")
            continue    # continue le while sans faire la suite

        resultat = bouger(valeur.plateau, "B", direction)
        if resultat is None:
            print("Mur ou bord du plateau.")
            continue

        return resultat


def main():
    menu_de_debut()

    joueur = Joueur(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    ordi = Ordi(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)

    while True:
        action = demander_action(joueur, ordi)

        if action == "q":           # quitter le jeu
            print("À bientôt !")
            return

        if action == "d":           # se deplacer
            ecrasement = demander_direction()
            joueur.lulu -= valeur.LULU_POUR_BOUGER
            joueur.protege = True

            if ecrasement:
                afficher_plateau()
                print("Tu as écrasé le Dark Magician. Tu gagnes !")
                return

            carte_ordi = ordi.jouer()
            print(f"\nLe Dark Magician lance {carte_ordi}.")
            print("Tu t'es déplacé : son attaque ne te touche pas.")
            joueur.protege = False

        else:                       # attaquer
            carte_joueur = joueur.choisir_carte() # le joueur et l'ordi choisissnet leurs cartes
            carte_ordi = ordi.jouer()
            print(f"\nTu lances {carte_joueur}. Le Dark Magician lance {carte_ordi}.")

            degats_joueur, degats_ordi = attaque.resoudre(carte_joueur, carte_ordi)

            if joueur.protege:
                degats_joueur = 0
            if ordi.protege:
                degats_ordi = 0

            joueur.vie -= degats_joueur
            ordi.vie -= degats_ordi
            joueur.lulu += degats_ordi
            ordi.lulu += degats_joueur
            joueur.protege = False
            ordi.protege = False

            print(f"Tu infliges {degats_ordi} dégâts et tu subis {degats_joueur} dégâts.")

        print()

        if not joueur.est_vivant() and not ordi.est_vivant():
            print("Match nul !")
            return
        if not joueur.est_vivant():
            print("Tu n'as plus de PV. Le Dark Magician gagne...")
            return
        if not ordi.est_vivant():
            print("Le Dark Magician n'a plus de PV. Tu gagnes !")
            return


if __name__ == "__main__":
    main()
