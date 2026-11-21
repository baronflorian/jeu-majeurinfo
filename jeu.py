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


def soigner(joueur):
    if joueur.vie >= valeur.VIE_DEPART:
        print("Tu es déjà à 80 PV.")
        return False
    if joueur.lulu < valeur.LULU_POUR_SOIGNER:
        print(f"Il te faut {valeur.LULU_POUR_SOIGNER} lulu pour te soigner.")
        return False

    joueur.lulu -= valeur.LULU_POUR_SOIGNER
    vie_avant = joueur.vie
    joueur.vie = min(valeur.VIE_DEPART, joueur.vie + valeur.PV_SOIGNES)
    pv_recuperes = joueur.vie - vie_avant
    print(f"Tu récupères {pv_recuperes} PV et utilises {valeur.LULU_POUR_SOIGNER} lulu.")
    return True


def demander_action(joueur, ordi):
    while True:
        afficher_plateau()
        afficher_etat(joueur, ordi)
        print("a = attaquer   d = se déplacer   s = se soigner   q = quitter")
        choix = input("Ton choix : ").lower()

        if choix == "a":
            return "a"
        if choix == "q":
            return "q"
        if choix == "s":
            if soigner(joueur):
                return "s"
            continue
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


def tour_ordi(ordi, joueur, graphe, carte_joueur, action):
    # L'Ordi se soigne avec 5 lulu s'il a moins de 10 PV.
    if ordi.lulu >= valeur.LULU_POUR_SOIGNER and ordi.vie <= valeur.VIE_DEPART - valeur.PV_SOIGNES:
        ordi.lulu -= valeur.LULU_POUR_SOIGNER
        ordi.vie = min(valeur.VIE_DEPART, ordi.vie + valeur.PV_SOIGNES)
        print(f"Le Dark Magician récupère {valeur.PV_SOIGNES} PV.")
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
            joueur.lulu_soin += degats / 2
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
    if action == "s":
        return False
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
    joueur.lulu_soin += degats_ordi / 4 # il faut au moins attendre un 2 tour pr se soigner pr ca que je div par 4 et pas par 2

    lulu_total_ordi = degats_joueur * ordi.multiplicateur_lulu # calcule en fc du cooef qui dpeend de la difficulte choise pas lutilisateur.
    ordi.lulu += lulu_total_ordi
    ordi.lulu_soin += lulu_total_ordi / 4    
    ordi.protege = False

    print(f"Tu infliges {degats_ordi} dégâts et tu subis {degats_joueur} dégâts.")
    return False


def afficher_attaque_ordi(ordi, carte_ordi):
    print(f"\nLe Dark Magician lance {carte_ordi}.")
    complementaire = valeur.carte_complementaire[carte_ordi]
    degats_complementaire = valeur.degat_elements[complementaire]
    degat_attaque = valeur.degat_elements[carte_ordi]
    print(f"Attaque : {carte_ordi} ({degat_attaque} dégâts).")
    print(f"Attaque complémentaire : {complementaire} ({degats_complementaire} dégâts).")


def tour_ordi_en_premier(ordi, joueur):
    """Fait jouer une attaque à l'Ordi avant que le joueur ne joue."""
    if ordi.lulu >= valeur.LULU_POUR_SOIGNER and ordi.vie <= valeur.VIE_DEPART - valeur.PV_SOIGNES:
        ordi.lulu -= valeur.LULU_POUR_SOIGNER
        ordi.vie = min(valeur.VIE_DEPART, ordi.vie + valeur.PV_SOIGNES)
        print(f"Le Dark Magician récupère {valeur.PV_SOIGNES} PV.")

    carte_ordi = ordi.choisir_carte()
    afficher_attaque_ordi(ordi, carte_ordi)
    return carte_ordi


def resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi):
    """Résout l'attaque du joueur après une attaque de l'Ordi en premier."""
    degats_joueur, degats_ordi = attaque.resoudre(carte_joueur, carte_ordi)

    if joueur.protege:
        degats_joueur = 0
    if ordi.protege:
        degats_ordi = 0

    joueur.vie -= degats_joueur
    ordi.vie -= degats_ordi
    joueur.lulu += degats_ordi
    joueur.lulu_soin += degats_ordi / 4
    ordi.lulu += degats_joueur * ordi.multiplicateur_lulu
    ordi.lulu_soin += degats_joueur * ordi.multiplicateur_lulu / 4

    print(f"Tu infliges {degats_ordi} dégâts et tu subis {degats_joueur} dégâts.")


def main():
    menu_de_debut()
    choix_plateaux = {"1": "petit", "2": "moyen", "3": "grand"}
    choix = input("Choisis un plateau, 1 pour petit, 2 pour moyen, 3 pour grand. \n")
    while choix not in choix_plateaux:
        choix = input("Choix invalide. Tape 1, 2 ou 3.\n")
    valeur.changer_plateau(choix_plateaux[choix])
    joueur = Joueur(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    ordi = Ordi(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    difficultes = {"1": 0.85, "2": 1, "3": 1.15}
    choix_difficulte = input("Difficulté (1 = facile, 2 = moyen, 3 = difficile) : ")
    while choix_difficulte not in difficultes:
        choix_difficulte = input("Tape 1, 2 ou 3 : ")
    ordi.multiplicateur_lulu = difficultes[choix_difficulte]
    graphe = construire_graphe(valeur.plateau)
    ordi_commence = True

    while True:
        carte_ordi = None

        if ordi_commence:
            print("\nLe Dark Magician commence ce tour.")
            carte_ordi = tour_ordi_en_premier(ordi, joueur)

            if not joueur.est_vivant():
                print("Tu n'as plus de PV. Le Dark Magician gagne...")
                return

            action = demander_action(joueur, ordi)
            if action == "q":
                print("À bientôt !")
                return

            if action == "d":
                ecrasement = demander_direction()
                joueur.lulu -= valeur.LULU_POUR_BOUGER
                joueur.protege = True
                ordi.protege = False

                if ecrasement:
                    afficher_plateau()
                    print("Tu as écrasé le Dark Magician. Tu gagnes !")
                    return
            elif action == "s":
                print("Tu es protégé par ton soin : tu ne subis aucune attaque.")
            else:
                carte_joueur = joueur.choisir_carte()
                resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi)
        else:
            print("\nTu commences ce tour.")
            action = demander_action(joueur, ordi)
            if action == "q":
                print("À bientôt !")
                return

            carte_joueur = None
            if action == "d":
                ecrasement = demander_direction()
                joueur.lulu -= valeur.LULU_POUR_BOUGER
                joueur.protege = True

                if ecrasement:
                    afficher_plateau()
                    print("Tu as écrasé le Dark Magician. Tu gagnes !")
                    return
            elif action == "s":
                print("Tu es protégé par ton soin : tu ne subis aucune attaque.")
            else:
                carte_joueur = joueur.choisir_carte()

            if action != "s":
                ecrasement_ordi = tour_ordi(ordi, joueur, graphe, carte_joueur, action)
                if ecrasement_ordi:
                    afficher_plateau()
                    print("Le Dark Magician t'a écrasé. Tu perds...")
                    return

        ordi_commence = not ordi_commence

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
