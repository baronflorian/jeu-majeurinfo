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
        print(f"Tu es déjà à {valeur.VIE_DEPART} PV.")
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
    soin_utilise = False
    while True:
        afficher_plateau()
        afficher_etat(joueur, ordi)
        option_soin = "" if soin_utilise else "s pour se soigner   "
        print(f"a pour attaquer   d pour se déplacer   {option_soin}q pour quitter")
        choix = input("Ton choix : ").strip().lower()

        if choix in ("a", "q"):
            return choix, soin_utilise
        if choix == "s":
            if soin_utilise:
                print("Tu as déjà utilisé ton soin ce tour.")
            else:
                soin_utilise = soigner(joueur)
        elif choix == "d":
            if joueur.peut_bouger():
                return choix, soin_utilise
            print(f"\nIl te faut {valeur.LULU_POUR_BOUGER} lulu pour te déplacer.\n")
        else:
            print("\nChoix invalide.\n")


def proposer_soin_apres_action(joueur, ordi):
    if joueur.vie >= valeur.VIE_DEPART or joueur.lulu < valeur.LULU_POUR_SOIGNER:
        return

    afficher_etat(joueur, ordi)
    while True:
        choix = input("tape : s pour se soigner ou Entrée = terminer le tour : ")
        if choix == "s":
            soigner(joueur)
            return
        if choix == "": #permet au joueur de taper sur la touhe entree pour continuer
            return
        print("Tape s pour te soigner ou appuie sur Entrée.")


def demander_direction():
    while True:
        direction = input("Direction (z haut, s bas, q gauche, d droite) : ")

        if direction not in valeur.DIRECTIONS:
            print("Direction invalide.")
            continue    # continue le while sans faire la suite

        resultat = bouger(valeur.plateau, "B", direction)
        if resultat is None:
            print("Passage bloqué par un mur ou par le Dark Magician.")
            continue

        return resultat


def tour_ordi(ordi, joueur, graphe, carte_joueur):
    """L'Ordi se déplace s'il a assez de lulu, sinon il attaque.
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
        destination = deplacer_vers(valeur.plateau, "A", suivante[0], suivante[1])
        ordi.lulu -= valeur.LULU_POUR_BOUGER
        ordi.protege = True
        print("\nLe Dark Magician se déplace.")
        joueur.protege = False
        return destination is True
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
    ordi.lulu += degats_joueur * ordi.multiplicateur_lulu
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


def tour_ordi_en_premier(ordi, graphe, joueur):
    """Déplace ou fait attaquer l'Ordi avant l'action du joueur.

    Renvoie (carte jouée, joueur écrasé). La carte vaut None si l'Ordi s'est déplacé.
    """
    position_ordi = trouver_position(valeur.plateau, "A")
    position_joueur = trouver_position(valeur.plateau, "B")

    suivante = None
    if ordi.peut_bouger():
        suivante = ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

    if suivante is not None:
        ordi.protege = False
        destination = deplacer_vers(valeur.plateau, "A", suivante[0], suivante[1])
        ordi.lulu -= valeur.LULU_POUR_BOUGER
        ordi.protege = True
        print("\nLe Dark Magician se déplace.")
        joueur.protege = False
        return None, destination is True

    carte_ordi = ordi.choisir_carte()
    afficher_attaque_ordi(ordi, carte_ordi)
    return carte_ordi, False


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
    ordi.lulu += degats_joueur * ordi.multiplicateur_lulu

    print(f"Tu infliges {degats_ordi} dégâts et tu subis {degats_joueur} dégâts.")
    ordi.protege = False


def resoudre_attaque_joueur_seule(ordi, joueur, carte_joueur):
    """Applique l'attaque du joueur si l'Ordi s'est déplacé au début du tour."""
    degats = valeur.degat_elements[carte_joueur]
    ordi.vie -= degats
    joueur.lulu += degats
    ordi.protege = False
    print(f"\nTon attaque inflige {degats} dégâts au Dark Magician.")


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
            carte_ordi, joueur_ecrase = tour_ordi_en_premier(ordi, graphe, joueur)
            if joueur_ecrase:
                afficher_plateau()
                print("Le Dark Magician t'a écrasé. Tu perds...")
                return
        else:
            print("\nTu commences ce tour.")

        action, soin_utilise = demander_action(joueur, ordi)
        if action == "q":
            print("À bientôt !")
            return

        carte_joueur = None
        if action == "d":
            destination = demander_direction()
            joueur.lulu -= valeur.LULU_POUR_BOUGER
            if destination == "|":
                afficher_plateau()
                print("Tu es sorti du labyrinthe. Tu gagnes !")
                return

            joueur.protege = True
            if ordi_commence:
                ordi.protege = False
        else:
            carte_joueur = joueur.choisir_carte()

        if ordi_commence:
            if carte_ordi is not None:
                if carte_joueur is not None:
                    resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi)
            elif carte_joueur is not None:
                resoudre_attaque_joueur_seule(ordi, joueur, carte_joueur)
        elif tour_ordi(ordi, joueur, graphe, carte_joueur):
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

        if not soin_utilise:
            proposer_soin_apres_action(joueur, ordi)
        ordi_commence = not ordi_commence


if __name__ == "__main__":
    main()
