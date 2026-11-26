## Description du jeu:

Le jeu est un affrontement entre deux personnages : le joueur et le Dark Magicien, contrôlé par une intelligence artificielle.

La partie se déroule sur une carte représentant un labyrinthe. Le joueur a deux possibilités pour gagner : 
- atteindre la sortie du labyrinthe 
- vaincre le Dark Magicien grâce à ses attaques. 

De son côté, le Dark Magicien doit éliminer le joueur pour remporter la partie.

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
- pour l'ia : gain de lulus = dégats infligés x coefficient de difficulté
- 4 cartes en main, pioche de 8

3 difficultés qui multiplient les lulus gagnés par l'ia par un coefficient ( 1.05 / 1.25 / 1.35)
3 choix de plateau de taille differente : petit 5×5, moyen 9×9, grand 11×11, (choisis au lancement)


## Règles du jeu:
*Le Dark Magician commence la partie puis pour chaque round, il y a alternance entre le joueur et le Dark Magician. (au second round, le joueur commencera)*

### Dans le labyrinthe :

Le joueur est représenté par la lettre J.
Le Dark Magicien est représenté par la lettre M.
La sortie est représentée par le symbole |.

Le joueur gagne s'il atteint la sortie du labyrinthe ou s'il parvient à vaincre le Dark Magicien grâce à ses attaques.

Le joueur perd si le Dark Magicien arrive sur sa case ou si ses attaques lui font perdre tous ses points de vie.

Il est impossible de traverser la case occupée par le Dark Magicien.

### Cartes : 
Le joueur et le Dark Magicien disposent de différentes cartes, plus ou moins puissantes, pour attaquer leur adversaire.

À chaque tour, chacun peut choisir une carte parmi les 4 cartes disponibles dans sa main, sur les 8 cartes que compte le jeu.

Lorsqu'une carte est utilisée, elle est immédiatement remplacée par une nouvelle carte. Il est donc impossible d'utiliser deux fois de suite la même carte.

Certaines cartes sont complémentaires. Lorsque les deux personnages jouent des cartes complémentaires au cours d'un même tour, un effet spécial se déclenche : celui qui a joué la carte la plus puissante inflige à son adversaire des dégâts correspondant à la différence de puissance entre les deux cartes, auxquels s'ajoutent 2 points bonus et il ne subit aucun dégât pendant ce tour.

Les tours du joueur et du Dark Magicien alternent afin que chacun puisse, lorsque cela est possible, bénéficier de l'utilisation d'une carte complémentaire.

### Lulus
À chaque tour, le joueur et le Dark Magicien gagnent des points proportionnellement à la puissance de leur attaque. Ces points sont appelés des lulus.

#### acheter des cartes
Les lulus constituent une ressource essentielle pour progresser dans le jeu, car les cartes les plus puissantes nécessitent d'en dépenser pour être utilisées.

Pour le joueur :

La carte Foudre coûte 2 lulus.
La carte Terre coûte 2 lulus.
La carte Magie coûte 4 lulus.
La carte Temps coûte 4 lulus.
Les autres cartes sont gratuites.

Si aucune carte de sa main n'est jouable (car pas assez de lulus), le joueur passe son tour et reçoit une nouvelle carte en remplacement à la fin de celui-ci.

#### se soigner
Les lulus servent également à se soigner (10 lulus pour 14PV). Seul le joueur possède cette capacité.
Il peut se soigner avant ou après l'action.


#### se déplacer
Enfin, pour bouger dans le labyrinthe, il faut dépenser 22 lulus.
Lorsqu'un personnage (le joueur ou le Dark Magicien) se déplace, il bénéficie d'une **protection** pendant le tour suivant :
après un déplacement, la prochaine attaque adverse est alors annulée (0 dégât subi). Si le joueur se déplace, l'attaque du Dark Magician ne le touche donc pas. Si le Dark Magician se déplace en premier, le joueur ne peut pas l'attaquer ce tour-là.

### Fin de partie
**victoire** si sortie ou dark magician tué
**défaite** si plus de PV ou si dark magician sur la case

match nul???