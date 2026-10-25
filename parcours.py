import valeur
class parcour:
    def passage(map):
        for ligne in map.splitlines():
            for caractere in ligne :
                if caractere == " ":
                    pass
    def trouver_position(lettre): # la lertre correspond A  ou B A le ia et B le user
        for y, ligne in enumerate(map.splitlines()):
            for x, caractere in enumerate(ligne) :
                if caractere == lettre:
                    return x,y 