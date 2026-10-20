class JoueurOrdi:
    def jouer(self, action_joueur):
        if action_joueur == 1: #feu
            return 2  # Lancer de la glace
        elif action_joueur == 2:# glace
            return 3  # Lancer un éclair
        elif action_joueur == 3:#eclair
            return 1  # Lancer une boule de feu
        else:
            return None