class Player:
    """_Class générique d'un joueur humain ou ordi_
    """
    def __init__(self, actions, vie):
        self.vie = vie
        self.filesdemescartes = actions  # La file sde toutes les action voir dans jeu.py, fn menu desa ction duispo
        self.lescartes_disponibles = []

        # Prendre quatre cartes dans la file
        for i in range(4):
            carte_suivante = self.filesdemescartes.popleft()
            self.lescartes_disponibles.append(carte_suivante) 
    
    def est_vivant(self):
        return self.vie > 0
