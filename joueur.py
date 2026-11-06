from player import Player


class Joueur(Player):
    def __init__(self, actions, vie, lulu):
        super().__init__(actions, vie)
        self.lulu = lulu

    def est_vivant(self):
        return self.vie > 0
    
    def deplacement(self):
        if self.lulu >= 20:
            self.lulu -= 20
            return True

    def choisir_carte(self):
        print("Tes cartes disponibles :")

        for i in range(len(self.lescartes_disponibles)):
            print(i+1,":",self.lescartes_disponibles[i])

        choix = input("Choisis une carte 1 à 4: ")
        #il faut pesner a rajouter une condition pr sassurer que oel nombre sois comprens entre 1 et 4. 
        #dfait un while jpense
           

        # mnt il faut enlever l'élément de la liste contenant 4 cartes
        carte = self.lescartes_disponibles.pop(int(choix) - 1)

        # on prend une carte parmis celle  de la loste dattente (file) pr la mettre das la lisrte lescartesdispo
        
        self.lescartes_disponibles.append(self.filesdemescartes.popleft())
        # on met la carte choisis en fil dattente dans la file
        self.filesdemescartes.append(carte)

        return carte

        from player import Player
from valeur import *


class Ordi(Player):
    def __init__(self, actions, vie):
        super().__init__(actions, vie)

    # def __init__(self, actions, vie):
    #     self.vie = vie
    #     self.cartes_ = actions 
    #     self.cartes_a_jouer = []

    #     for i in range(4):
    #         carte_suivante=self.filesdemescartes.popleft()
    #         self.lescartes_disponibles.append(carte_suivante) 

    def jouer(self, action_joueur, cartes):
        # en fonction de l'action du joueur et des cartes de l'ia, jouer la carte complementaire ou celle qui fait le plus de degats

        carte_degat_max = cartes[0]
        for carte in cartes:
            if {action_joueur, carte} in COMPLEMENTAIRES:
                return carte

            if CARTES[carte][1] > CARTES[carte_degat_max][1]:
                carte_degat_max = carte
        return carte_degat_max
    
    def avancer(self):
        pass
