
import valeur
import joueur

class attaque:
    def attaquer(self,cible):    #    cible c'est l'ia mais on sait pas comment on l'appelle donc pour l'instant c'est cible        
        carte = joueur.choisir_carte()
        degat=valeur.degat_elements[carte]
        cible.vie -= degat



    