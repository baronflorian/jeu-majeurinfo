## Description du jeu:

Le jeu est un affrontement entre deux personnages : le joueur et le Dark Magician, contrôlé par une intelligence artificielle.

La partie se déroule sur une carte représentant un labyrinthe. Le joueur a deux possibilités pour gagner : 
- atteindre la sortie du labyrinthe 
- vaincre le Dark Magician grâce à ses attaques.

De son côté, le Dark Magician doit éliminer le joueur pour remporter la partie.

## Prise en main du jeu
### Plateau
"#" = mur
espace = case libre
| = sortie
J = joueur
M = Dark Magician

### Cartes
| Carte  | Dégâts | Coût |
|--------|--------|------|
| Feu    | 10     | 0    |
| Eau    | 12     | 0    |
| Glace  | 8      | 0    |
| Lave   | 12     | 0    |
| Foudre | 14     | 2    |
| Terre  | 16     | 2    |
| Magie  | 20     | 4    |
| Temps  | 18     | 4    |

**Paires complémentaires :**
- Feu/Eau
- Glace/Lave
- Foudre/Terre
- Magie/Temps

### Valeurs par défaut
- au départ : 80 PV, 0 lulu
- soin : 10 lulus -> 14 PV (les PV sont plaffonés à 80)
- déplacement : 22 lulus
- pour le joueur : gain de lulus = dégats infligés
- pour le Dark Magician : gain de lulus = dégats infligés x coefficient de difficulté
- 4 cartes en main, pioche de 8

3 difficultés qui multiplient les lulus gagnés par le Dark Magician par un coefficient ( 1.05 / 1.25 / 1.35)
3 choix de plateau de taille differente : petit 5×5, moyen 9×9, grand 11×11, (choisis au lancement)


## Règles du jeu:
*Le Dark Magician commence la partie puis pour chaque round, il y a alternance entre le joueur et le Dark Magician. (au second round, le joueur commencera)*

### Dans le labyrinthe :

Le joueur est représenté par la lettre J.
Le Dark Magician est représenté par la lettre M.
La sortie est représentée par le symbole |.

Le joueur gagne s'il atteint la sortie du labyrinthe ou s'il parvient à vaincre le Dark Magician grâce à ses attaques.

Le joueur perd si le Dark Magician arrive sur sa case ou si ses attaques lui font perdre tous ses points de vie.

Il est impossible de traverser la case occupée par le Dark Magician.

### Cartes : 
Le joueur et le Dark Magician disposent de différentes cartes, plus ou moins puissantes, pour attaquer leur adversaire.

À chaque tour, chacun peut choisir une carte parmi les 4 cartes disponibles dans sa main, sur les 8 cartes que compte le jeu.

Lorsqu'une carte est utilisée, elle est immédiatement remplacée par une nouvelle carte. Il est donc impossible d'utiliser deux fois de suite la même carte.

Lorsque les deux personnages jouent des cartes complémentaires de puissances différentes, celui qui a joué la plus puissante inflige la différence de puissance plus 2 dégâts et ne subit aucun dégât. Si les deux cartes ont la même puissance, les attaques s’annulent.

Les tours du joueur et du Dark Magician alternent afin que chacun puisse, lorsque cela est possible, bénéficier de l'utilisation d'une carte complémentaire.

### Lulus
Les attaques rapportent des lulus en fonction des dégâts infligés. Le coefficient de difficulté s’applique au gain du Dark Magician.

#### acheter des cartes
Les lulus constituent une ressource essentielle pour progresser dans le jeu, car les cartes les plus puissantes nécessitent d'en dépenser pour être utilisées.

Pour le joueur :

La carte Foudre coûte 2 lulus.
La carte Terre coûte 2 lulus.
La carte Magie coûte 4 lulus.
La carte Temps coûte 4 lulus.
Les autres cartes sont gratuites.

Si aucune carte de sa main n'est jouable (car pas assez de lulus), le joueur passe son tour et reçoit une nouvelle carte en remplacement à la fin de celui-ci.

#### Se soigner
Un soin coûte 10 lulus et rend jusqu’à 14 PV, sans dépasser 80 PV.
Le joueur peut se soigner une fois par tour, avant ou après son action.
Le Dark Magician se soigne avant de choisir son action s’il lui reste moins de 10 PV et qu’il a au moins 10 lulus.


#### se déplacer
Enfin, pour bouger dans le labyrinthe, il faut dépenser 22 lulus.
Lorsqu'un personnage (le joueur ou le Dark Magician) se déplace, il bénéficie d'une **protection** pendant le tour suivant :
après un déplacement, la prochaine attaque adverse est alors annulée (0 dégât subi). Si le joueur se déplace, l'attaque du Dark Magician ne le touche donc pas. Si le Dark Magician se déplace en premier, le joueur ne peut pas l'attaquer ce tour-là.

### Fin de partie

- **Victoire** si le joueur atteint la sortie ou si le Dark Magician tombe à 0 PV ou moins et que le joueur survit.
- **Défaite** si le Dark Magician arrive sur la case du joueur ou si le joueur tombe à 0 PV ou moins et que le Dark Magician survit.
- **Match nul** si les deux personnages tombent à 0 PV ou moins au même tour.
