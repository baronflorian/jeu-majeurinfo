import valeur
from parcours import a_star
from player import Player


class Joueur(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.lulu = lulu
        self.lulu_soin = 0
        self.protege = False # si le joueur vient de se déplacer, il sera protégé

    def peut_bouger(self):
        return self.lulu >= valeur.LULU_POUR_BOUGER

    def choisir_carte(self):
        print("\nTes cartes :")
        for i, carte in enumerate(self.cartes_en_main):
            print(f"  {i + 1}. {carte} ({valeur.degat_elements[carte]} dégâts)") # afficher les cartes disponibles

        while True:
            choix = input("Choisis une carte (1 à 4) : ")
            if choix.isdigit() and 1 <= int(choix) <= 4: # verifier que la carte choisie est valide
                return self.jouer_carte(int(choix) - 1)
            print("Choix invalide, réessaie.")


class Ordi(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.lulu = lulu
        self.lulu_soin = 0
        self.protege = False

    def peut_bouger(self):
        return self.lulu >= valeur.LULU_POUR_BOUGER

    def choisir_carte(self, carte_joueur=None):
        """Heuristique : jouer la complémentaire si elle est plus forte,
        sinon jouer la carte qui fait le plus de dégâts."""
        if carte_joueur is not None:
            complementaire = valeur.carte_complementaire[carte_joueur]
            if complementaire in self.cartes_en_main:
                if valeur.degat_elements[complementaire] > valeur.degat_elements[carte_joueur]:
                    numero = self.cartes_en_main.index(complementaire)
                    return self.jouer_carte(numero)

        # Sinon, on cherche la carte aux dégâts maximaux
        numero_max = 0
        for i, carte in enumerate(self.cartes_en_main):
            if valeur.degat_elements[carte] > valeur.degat_elements[self.cartes_en_main[numero_max]]:
                numero_max = i
        return self.jouer_carte(numero_max)

    def choisir_deplacement(self, graphe, position_ordi, position_joueur):
        """A* : renvoie la prochaine case du chemin vers le joueur, ou None."""
        chemin = a_star(graphe, position_ordi, position_joueur)
        if len(chemin) >= 2:
            return chemin[1]
        return None
