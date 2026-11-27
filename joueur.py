import valeur
from parcours import a_star
from player import Player


class Joueur(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.lulu = lulu
        self.protege = False # si le joueur vient de se déplacer, il sera protégé

    def peut_bouger(self):
        return self.lulu >= valeur.LULU_POUR_BOUGER

    def peut_attaquer(self):
        for carte in self.cartes_en_main:
            if self.lulu >= valeur.cout_cartes.get(carte, 0):
                return True
        return False

    def remplacer_carte(self):
        carte_remplacee = self.jouer_carte(0)
        carte_piochee = self.cartes_en_main[-1]
        print(f"Pour ton prochain tour, {carte_remplacee} est remplacée par {carte_piochee}.")

    def choisir_carte(self):
        print("\nTes cartes :")
        for i, carte in enumerate(self.cartes_en_main):
            cout = valeur.cout_cartes.get(carte, 0)
            cout_affiche = f" | -{cout} lulu" if cout else ""
            print(f"  {i + 1}. {carte} ({valeur.degat_elements[carte]} dégâts{cout_affiche})")

        while True:
            choix = input("Choisis une carte (1 à 4) : ").strip()
            if choix in ("1", "2", "3", "4"):
                indice = int(choix) - 1
                carte = self.cartes_en_main[indice]
                if carte in valeur.cout_cartes:
                    if self.lulu >= valeur.cout_cartes[carte]:
                        self.lulu -= valeur.cout_cartes[carte]
                        return self.jouer_carte(indice)
                    else:
                        print("tu n'a pas assez de lulu pour jouer cette carte")
                        continue
                return self.jouer_carte(indice)
            print("Choix invalide, réessaie.")


class Ordi(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.vie_max = vie
        self.lulu = lulu
        self.protege = False
        self.niveau_difficulte = 2

    def peut_bouger(self):
        return self.lulu >= valeur.LULU_POUR_BOUGER

    def soin_ordi(self):
        if not self.peut_se_soigner():
            return False

        vie_avant = self.vie
        self.lulu -= valeur.LULU_POUR_SOIGNER
        self.vie = min(self.vie_max, self.vie + valeur.PV_SOIGNES)
        pv_recuperes = self.vie - vie_avant
        print(f"Le Dark Magician récupère {pv_recuperes} PV.")
        return True

    def peut_se_soigner(self):
        return self.lulu >= valeur.LULU_POUR_SOIGNER and self.vie < self.vie_max

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

    def choisir_deplacement(self, graphe, position_ordi, position_cible):
        """Renvoie le premier pas vers la cible accessible la plus proche, ou None."""
        cibles = [position_cible] if isinstance(position_cible, tuple) else position_cible
        if position_ordi in cibles:
            return None
        chemins = (a_star(graphe, position_ordi, cible) for cible in cibles)
        chemin = min((chemin for chemin in chemins if chemin), key=len, default=[])
        if len(chemin) >= 2:
            return chemin[1]
        return None
