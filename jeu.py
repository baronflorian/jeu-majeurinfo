import attaque
import valeur
import parcours
from joueur import Joueur, Ordi


def tour_ordi_ia_ameliorer(ordi, joueur, graphe):
    """change l'ordre des priorité appliqué par le dark magicien, il ne se deplace plus forcement en priorité 
    ces choix dépendent de la place des joueur sur le plateau"""
    """si le magicien ne peut pas se deplacer ou si ce n'est pas dans son interet il renvoie None et il applique l'ordre des priorité normal sur le choix de l'attaque """
    
    position_sortie = parcours.trouver_position(valeur.plateau, "|")
    position_joueur = parcours.trouver_position(valeur.plateau, "J")
    position_ordi = parcours.trouver_position(valeur.plateau, "M")
    if position_sortie is None or position_joueur is None or position_ordi is None:
        return None

    if len(valeur.plateau) == 5:
        plateau = 1
    elif len(valeur.plateau) == 9:
        plateau = 2
    else:
        plateau = 3

    if ordi.vie < 40 and ordi.peut_se_soigner():
        ordi.soin_ordi()

    if not ordi.peut_bouger():
        return None

    if parcours.distance_manhattan(position_joueur, position_sortie) <= valeur.distance_limite[plateau]:       #si le joueur est trop pres de la sortie l'ia va venir defendre la sortie
        cases_a_defendre =parcours.trouver_case_avant_sortie(valeur.plateau, "|")                              #mais limite entre distance joueur et ordi pour que l'ia ne reste pas a bloquer la sortie tout le temps
        if parcours.distance_manhattan(position_joueur, position_ordi)<=3:
            return ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

        cases_a_defendre=cases_a_defendre[0]
        if cases_a_defendre==position_ordi:
            return None

        return ordi.choisir_deplacement(graphe, position_ordi, cases_a_defendre)

    if parcours.distance_manhattan(position_joueur, position_ordi) >=valeur.distance_poursuite_limite[plateau]:    #si le joueur est trop loin l'ordi ne cherche pas a le poursuivre le joueur devra forcement se rapprocher de la sortie donc de l'ia
        return None                                                                                                #elle peut donc economiser ses lulu et attaquer

    return ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

def menu_de_debut():                                     #menu affiché uniquement au debut de la partie
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
    lulu_ordi = f"{ordi.lulu:.1f}".replace(".", ",")
    print(f"Dark Magician : {ordi.vie} PV | {lulu_ordi} lulu")


def soigner(joueur):
    """verifie les conditions pour appliquer le soin (que la vie du joueur ne soit pas superieur a la vie max et que le joueur est assez de lulu)."""
    if joueur.vie >= valeur.VIE_DEPART:
        print(f"Tu es déjà à {valeur.VIE_DEPART} PV.")
        return False
    if joueur.lulu < valeur.LULU_POUR_SOIGNER:
        print(f"Il te faut {valeur.LULU_POUR_SOIGNER} lulu pour te soigner.")
        return False

    joueur.lulu -= valeur.LULU_POUR_SOIGNER
    vie_avant = joueur.vie
    # Le soin ne peut pas depasser le nombre de PV initial.
    joueur.vie = min(valeur.VIE_DEPART, joueur.vie + valeur.PV_SOIGNES)
    pv_recuperes = joueur.vie - vie_avant
    print(f"Tu récupères {pv_recuperes} PV et utilises {valeur.LULU_POUR_SOIGNER} lulu.")
    return True


def demander_action(joueur, ordi, soin_utilise=False):
    """Renvoie l'action du joueur et indique si son soin du tour a été utilisé.
    Le soin s'applique directement dans le menu, qui reste ouvert ensuite.
    """
    while True:
        afficher_plateau()
        afficher_etat(joueur, ordi)
        if not joueur.peut_attaquer():
            print("Aucune carte n'est jouable. Tu passes ton tour.")
            return "p", soin_utilise
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
    """Propose un soin de fin de tour si le joueur a des PV à récupérer et assez de Lulu."""
    if joueur.vie >= valeur.VIE_DEPART or joueur.lulu < valeur.LULU_POUR_SOIGNER:
        return

    afficher_etat(joueur, ordi)
    while True:
        choix = input("tape : s pour se soigner ou Entrée = terminer le tour : ").strip().lower()
        if choix == "s":
            soigner(joueur)
            return
        if choix == "": #permet au joueur de taper sur la touhe entree pour continuer
            return
        print("Tape s pour te soigner ou appuie sur Entrée.")


def demander_direction():
    """Déplace le joueur et renvoie l'ancien contenu de la case d'arrivée.

    Le résultat vaut None si le joueur annule et "|" s'il atteint la sortie.
    """
    while True:
        direction = input("Direction (z haut, s bas, q gauche, d droite, Entrée pour annuler) : ").strip().lower()

        if direction == "":
            return None

        if direction not in valeur.DIRECTIONS:
            print("Direction invalide.")
            continue    # pour eviter les erreurs

        resultat = parcours.bouger(valeur.plateau, "J", direction)
        if resultat is None:
            print("Passage bloqué par un mur ou par le Dark Magician.")
            continue

        return resultat


def tour_ordi(ordi, joueur, graphe, carte_joueur, joueur_passe=False):
    """Le Dark Magician se déplace s'il a assez de lulu, sinon il attaque.
    Renvoie True s'il écrase le joueur."""
    position_ordi = parcours.trouver_position(valeur.plateau, "M")
    position_joueur = parcours.trouver_position(valeur.plateau, "J")

    suivante = None
   
    if ordi.niveau_difficulte == 3:
        suivante = tour_ordi_ia_ameliorer(ordi, joueur, graphe)
    else:
        if ordi.vie < 20 and ordi.peut_se_soigner():
            ordi.soin_ordi()
        if ordi.peut_bouger():
            suivante = ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

    if suivante is not None:
        # Si le joueur a attaqué, son attaque touche le Dark Magician même si il choisit de se deplacer,il sera protégé au tour d'après.
        if carte_joueur is not None:
            degats = valeur.degat_elements[carte_joueur]
            ordi.vie -= degats
            joueur.lulu += degats
            print(f"\nTon attaque inflige {degats} dégâts au Dark Magician.")
            if not ordi.est_vivant():
                return False

        
        destination = parcours.deplacer_vers(valeur.plateau, "M", suivante[0], suivante[1])
        ordi.lulu -= valeur.LULU_POUR_BOUGER
        
        print("\nLe Dark Magician se déplace.")
        joueur.protege = False
        return destination == "J"
    # Le Dark Magician attaque
    carte_ordi = ordi.choisir_carte(carte_joueur)
    print(f"\nLe Dark Magician lance {carte_ordi}.")

    if carte_joueur is None and not joueur_passe:
        print("Tu t'es déplacé : son attaque ne te touche pas.")
        joueur.protege = False
        
        return False

    resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi)
    return False


def afficher_attaque_ordi(ordi, carte_ordi):
    print(f"\nLe Dark Magician lance {carte_ordi}.")
    complementaire = valeur.carte_complementaire[carte_ordi]
    degats_complementaire = valeur.degat_elements[complementaire]
    degat_attaque = valeur.degat_elements[carte_ordi]
    print(f"Attaque : {carte_ordi} ({degat_attaque} dégâts).")
    print(f"Attaque complémentaire : {complementaire} ({degats_complementaire} dégâts).")


def tour_ordi_en_premier(ordi, graphe, joueur):
    """Déplace ou fait attaquer le Dark Magician avant l'action du joueur.

    Renvoie (carte jouée, joueur écrasé). La carte vaut None si le Dark Magician s'est déplacé.
    """
    position_ordi = parcours.trouver_position(valeur.plateau, "M")
    position_joueur = parcours.trouver_position(valeur.plateau, "J")

    suivante = None

    if ordi.niveau_difficulte == 3:
        suivante = tour_ordi_ia_ameliorer(ordi, joueur, graphe)
    else:
        if ordi.vie < 20 and ordi.peut_se_soigner():
            ordi.soin_ordi()
        if ordi.peut_bouger():
            suivante = ordi.choisir_deplacement(graphe, position_ordi, position_joueur)

    if suivante is not None:
        
        destination = parcours.deplacer_vers(valeur.plateau, "M", suivante[0], suivante[1])
        ordi.lulu -= valeur.LULU_POUR_BOUGER
       
        print("\nLe Dark Magician se déplace.")
        joueur.protege = False
        return None, destination == "J"

    carte_ordi = ordi.choisir_carte()
    afficher_attaque_ordi(ordi, carte_ordi)
    return carte_ordi, False


def resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi):
    """Applique les dégâts de l'échange.

    `carte_ordi` vaut None quand le Dark Magician s'est déplacé : l'attaque du joueur le touche alors directement.
    """
    if carte_joueur is None:
        degats_joueur = valeur.degat_elements[carte_ordi]
        degats_ordi = 0
    elif carte_ordi is None:
        # Le Dark Magician s'est déplacé sans jouer de carte : l'attaque du joueur le touche directement.
        degats_joueur = 0
        degats_ordi = valeur.degat_elements[carte_joueur]
    else:
        degats_joueur, degats_ordi = attaque.resoudre(carte_joueur, carte_ordi)

    if joueur.protege:
        degats_joueur = 0
    
    joueur.vie -= degats_joueur
    ordi.vie -= degats_ordi
    # Le Lulu gagné dépend des dégâts donées. La difficulté joue sur le gain du Dark Magician.
    joueur.lulu += degats_ordi
    ordi.lulu += degats_joueur * ordi.multiplicateur_lulu

    print(f"Tu infliges {degats_ordi} dégâts et tu subis {degats_joueur} dégâts.")
    joueur.protege = False
    



def main():
    """Prépare la partie et gère les tours jusqu'à la fin du jeu."""
    menu_de_debut()
    choix_plateaux = {"1": "petit", "2": "moyen", "3": "grand"}
    choix = input("Choisis un plateau, 1 pour petit, 2 pour moyen, 3 pour grand. \n")
    while choix not in choix_plateaux:
        choix = input("Choix invalide. Tape 1, 2 ou 3.\n")
    valeur.changer_plateau(choix_plateaux[choix])
    joueur = Joueur(valeur.menu_actions_disponible(), valeur.VIE_DEPART, valeur.LULU_DEPART)
    choix_difficulte = input("Difficulté (1 = facile, 2 = moyen, 3 = difficile) : ")
    while choix_difficulte not in ("1", "2", "3"):
        choix_difficulte = input("Tape 1, 2 ou 3 : ")
    niveau_difficulte = int(choix_difficulte)
    vie_ordi = valeur.VIE_DEPART_ORDI_DIFFICILE if niveau_difficulte == 3 else valeur.VIE_DEPART
    ordi = Ordi(valeur.menu_actions_disponible(), vie_ordi, valeur.LULU_DEPART)
    ordi.niveau_difficulte = niveau_difficulte
    ordi.multiplicateur_lulu = valeur.difficultes[ordi.niveau_difficulte]
    # Le Dark Magician utilise le graphe pour trouver son chemin vers le joueur.
    graphe = parcours.construire_graphe(valeur.plateau)
    ordi_commence = True

    while True:        #gere un tour de jeu
        carte_ordi = None

        if ordi_commence:   #gere un tour de jeux dans le cas ou le Dark magicien commence recupere l'action de l'ordi
            print("\nTu joues en deuxième ce tour.")
            carte_ordi, joueur_ecrase = tour_ordi_en_premier(ordi, graphe, joueur)
            if joueur_ecrase:
                afficher_plateau()
                print("Le Dark Magician t'a écrasé. Tu perds...")
                return
        else:
            print("\nTu joues en premier ce tour.")

        soin_utilise = False
        while True:
            
            action, soin_utilise = demander_action(joueur, ordi, soin_utilise)

            if action != "d":
                break
            # Annuler le déplacement ramène au menu en conservant l'état du soin.
            destination = demander_direction()
            if destination is not None:
                break

        if action == "q":
            print("À bientôt !")
            return

        carte_joueur = None
        if action == "d":
            joueur.lulu -= valeur.LULU_POUR_BOUGER
            if destination == "|":
                afficher_plateau()
                print("Tu es sorti du labyrinthe. Tu gagnes !")
                return

            joueur.protege = True
            
        elif action == "a":
            carte_joueur = joueur.choisir_carte()

        # Si le Dark Magician a attaqué, le déplacement du joueur permet de l'esquiver.
        # S'il s'est déplacé, l'attaque du joueur le touche directement.
        if ordi_commence:
            if action != "d" and (carte_ordi is not None or carte_joueur is not None):
                resoudre_attaque_joueur(ordi, joueur, carte_joueur, carte_ordi)
        elif tour_ordi(ordi, joueur, graphe, carte_joueur, action == "p"):
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

        # Le joueur peut encore se soigner s'il n'a pas utilisé son soin dans le menu.
        if not soin_utilise:
            proposer_soin_apres_action(joueur, ordi)
        # Un passage forcé renouvelle une carte de la main pour le prochain tour.
        if action == "p":
            joueur.remplacer_carte()
        ordi_commence = not ordi_commence


if __name__ == "__main__":
    main()
