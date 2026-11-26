from collections import deque


class Player:
    """Classe de base du joueur humain et du Dark Magician."""

    def __init__(self, actions, vie):
        self.vie = vie
        self.pioche = deque(actions)   # les 4 cartes en réserve modelisées par une file
        self.cartes_en_main = []       # les 4 cartes visibles et jouables

        for i in range(4):
            self.cartes_en_main.append(self.pioche.popleft())   # On prend les 4 premières cartes de la pioche 

    def est_vivant(self):
        return self.vie > 0

    def jouer_carte(self, indice):
        """Joue la carte placée à cet indice (0 = première carte), puis fait tourner la main."""
        carte = self.cartes_en_main.pop(indice)
        self.cartes_en_main.append(self.pioche.popleft())        # La carte suivante de la pioche entre dans la main
        self.pioche.append(carte)                                # La carte jouée retourne au bout de la pioche
        return carte
