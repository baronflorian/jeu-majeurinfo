import attaque
import valeur
from joueur import Joueur, Ordi
from parcours import bouger, construire_graphe, deplacer_vers, trouver_position


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


def tour_ordi(ordi, joueur, graphe, carte_joueur):
    """L'Ordi se déplace s'il a 20 lulu, sinon il attaque.
    Renvoie True s'il écrase le joueur."""
    position_ordi = trouver_position(valeur.plateau, "A")
    position_joueur = trouver_position(valeur.plateau, "B")

    suivante = None
    if ordi.peut_bouger():
        suivante = ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

    if suivante is not None:
        # Si le joueur a attaqué, son attaque touche l'Ordi avant qu'il ne bouge.
        if carte_joueur is not None:
            degats = valeur.degat_elements[carte_joueur]
            if ordi.protege:
                degats = 0
            ordi.vie -= degats
            joueur.lulu += degats
            print(f"\nTon attaque inflige {degats} dégâts au Dark Magician.")
            if not ordi.est_vivant():
                return False

        ordi.protege = False
        ecrasement = deplacer_vers(valeur.plateau, "A", suivante[0], suivante[1])
        ordi.lulu -= valeur.LULU_POUR_BOUGER
        ordi.protege = True
        print("\nLe Dark Magician se déplace.")
        joueur.protege = False
        return ecrasement

    # L'Ordi attaque
    carte_ordi = ordi.choisir_carte(carte_joueur)
    print(f"\nLe Dark Magician lance {carte_ordi}.")

    if carte_joueur is None:
        print("Tu t'es déplacé : son attaque ne te touche pas.")
        joueur.protege = False
        ordi.protege = False
        return False

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
    return False


def main():
    menu_de_debut()
    choix_plateaux = {"1": "petit", "2": "moyen", "3": "grand"}
    choix = input("Choisis un plateau, 1 pour petit, 2 pour moyen, 3 pour grand")
    while choix not in choix_plateaux:
        choix = input("Choix invalide. Tape 1, 2 ou 3")
    valeur.changer_plateau(choix_plateaux[choix])
    joueur = Joueur(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    ordi = Ordi(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    graphe = construire_graphe(valeur.plateau)
    while True:
        action = demander_action(joueur, ordi)
        if action == "q":           # quitter le jeu
            print("À bientôt !")
            return

        carte_joueur = None
        if action == "d":           # se deplacer
            ecrasement = demander_direction()
            joueur.lulu -= valeur.LULU_POUR_BOUGER
            joueur.protege = True

            if ecrasement:
                afficher_plateau()
                print("Tu as écrasé le Dark Magician. Tu gagnes !")
                return
        else:                       # attaquer
            carte_joueur = joueur.choisir_carte()

        ecrasement_ordi = tour_ordi(ordi, joueur, graphe, carte_joueur)
        if ecrasement_ordi:
            afficher_plateau()
            print("Le Dark Magician t'a écrasé. Tu perds...")
            return

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
