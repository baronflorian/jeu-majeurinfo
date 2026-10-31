from valeur import *


class JoueurOrdi:
    def __init__(self, actions, vie):
        self.vie = vie
        self.cartes_ = actions 
        self.cartes_a_jouer = []

        for i in range(4):
            carte_suivante=self.filesdemescartes.popleft()
            self.lescartes_disponibles.append(carte_suivante) 
    


    def jouer(self, action_joueur, cartes):
        # en fonction de l'action du joueur et des cartes de l'ia, jouer la carte complementaire ou celle qui fait le plus de degats

        carte_degat_max = cartes[0]
        for carte in cartes:
            if {action_joueur, carte} in COMPLEMENTAIRES:
                return carte

            if CARTES[carte][1] > CARTES[carte_degat_max][1]:
                carte_degat_max = carte
        return carte_degat_max
    
    def avancer(self) 