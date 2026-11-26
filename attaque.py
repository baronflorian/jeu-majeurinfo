import valeur


def resoudre(carte_joueur, carte_ordi):
    """Renvoie (dégâts subis par le joueur, dégâts subis par l'ordi)."""
    degat_joueur = valeur.degat_elements[carte_joueur]
    degat_ordi = valeur.degat_elements[carte_ordi]


    # Les deux cartes sont complémentaires : seule la plus faible prend la différence et 2 point de degat en plus ou elles s'annulent 
    if valeur.carte_complementaire[carte_joueur] == carte_ordi:
        if degat_joueur > degat_ordi:
            return 0, (degat_joueur - degat_ordi) +2
        if degat_ordi > degat_joueur:
            return (degat_ordi - degat_joueur) +2, 0
        return 0, 0
        

    # Sinon, chacun prend les dégâts de la carte de l'autre
    return degat_ordi, degat_joueur
