import valeur
class parcour:
    def trouver_position(self, lettre): # la lertre correspond A  ou B A le ia et B le user
        for y, ligne in enumerate(valeur.map.splitlines()):
            for x, caractere in enumerate(ligne) :
                if caractere == lettre:
                    return x,y 

    def objet_a_la_postion_xy(self, x,y):
        return valeur.map.splitlines()[y][x] #  dabbord y vu ue cest les lignes !!!!     

    def supp_ou_add_un_obj(self, x, y, caractere):
        lignes = valeur.map.splitlines() # on divise la map en lgine
        lignes[y] = lignes[y][:x] + caractere + lignes[y][x+1:] 
        #onp prend la ligne quon veut et on separe cette lignes. pour ajouter au milieux le caractère
        valeur.map = "\n".join(lignes) 
        # on remet la map faisant rejoindre les lgines et en faisanat un saut a lal lgine
        
    def position_valide (self, x, y):
        lignes = valeur.map.splitlines()
        if 0<= y < len(lignes) and 0<= x < len(lignes[y]):
            return True
        else:
            return None
        
    
    def nouvelle_position(self, lettre):
        direction= int(input("Où veux tu bouger ? : 1 gauche , 2 droite , 3 avancer , 4 reculer "))
        x,y = self.trouver_position(lettre)
        if direction == 1:
            x,y = x-1 , y
        elif direction == 2: 
            x, y = x+1, y
        elif direction == 3:  
            x, y = x, y-1
        elif direction == 4:  
            x, y = x, y + 1
        else:
            print("La direction demandée n'existe pas !")
            return None
        return x,y
    
    def bouger(self, lettre):
        x_initial, y_initial = self.trouver_position(lettre) 
        # si la onuvelle postion est un mur on peut qd meme revenir  la postion initiale.  
        position = self.nouvelle_position(lettre)
        while position == None:
            position = self.nouvelle_position(lettre)
        x, y = position

        #on verifie quon est dans la map
        while not self.position_valide(x, y):
            print("Tu es hors de la map !")
            position = self.nouvelle_position(lettre)
            if position != None:
                x, y = position
            # on trouve la postiotn de la nouvelle case voulue du joeur

        # on veut savoir si on va d sun mur ou pas :
        while self.objet_a_la_postion_xy(x, y) == "#":
            print("Il y a un mur, choisis une autre position")
            position = self.nouvelle_position(lettre)
            
            while position == None:
                position = self.nouvelle_position(lettre)   
            x, y = position  
        # il faut a nouveau verifier quon est ds la map :
            while not self.position_valide(x, y):
                print("Tu es hors de la map !")
                position = self.nouvelle_position(lettre)

                if position != None:
                    x, y = position

        if self.objet_a_la_postion_xy(x,y) == "A" or self.objet_a_la_postion_xy(x,y) == "B":
            self.supp_ou_add_un_obj(x_initial, y_initial, " ")
            self.supp_ou_add_un_obj(x, y, lettre)
            if lettre == "A":
                joueur_mort = "B"
            if lettre == "B":
                joueur_mort = "A"
            print("Le joueur", lettre,"a gagné. Il a écrasé le joueur", joueur_mort, "1")

        else:
            self.supp_ou_add_un_obj(x_initial, y_initial, " ")
            self.supp_ou_add_un_obj(x, y, lettre)
            
        
            

# quand lutilisateur obtient un lulu lutilisateur peut bouger
# on demandera a lautilisateur si il veut aller a gauche dereeire devant ou a droite
# la demande sera effectue dans une variable direction avec un input
# 1 : gauche , 2 droite , 3 avancer , 4 reculer