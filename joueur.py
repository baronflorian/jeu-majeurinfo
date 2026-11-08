import random

import valeur
from player import Player


class Joueur(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.lulu = lulu
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
        self.protege = False

    def jouer(self): # joue au hasard pour l'instant
        carte_hasard = random.randrange(len(self.cartes_en_main)) # choisit un nb au hasard entre 0 et 4
        return self.jouer_carte(carte_hasard)
