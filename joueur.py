class Joueur:
    def __init__(self, actions):
        self.filesdemescartes = actions  # La file sde toutes les action voir dans jeu.py, fn menu desa ction duispo
        self.lescartes_disponibles = []

        # Prendre quatre cartes dans la file
        for i in range(4):
            carte_suivante=self.filesdemescartes.popleft()
            self.lescartes_disponibles.append(carte_suivante) 

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