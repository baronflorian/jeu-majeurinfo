# Heuristique de choix des actions du Dark Magician:
*Le Dark Magician suit une stratégie basée sur des règles de priorité afin de choisir l'action qui lui semble la plus avantageuse.*

Le Dark Magician se soigne en priorité s'il lui reste moins de 20 PV(40 au niveau 3) et dispose d'assez de Lulu.

Aux niveaux 1 et 2, le Dark Magician cherche en priorité à se déplacer lorsqu'il en a la possibilité. Ce choix lui permet de se rapprocher du joueur et de tenter de l'atteindre afin de remporter la partie.

Au niveau 3, il ne se déplace plus forcément en priorité : selon la position du joueur, il peut préférer rester sur place et attaquer.

Si le déplacement n'est pas possible, ou si le niveau 3 estime qu'il n'est pas utile, le Dark Magician cherche à infliger le maximum de dégâts au joueur.

Pour cela, son choix dépend de l'ordre de jeu :
- S'il joue en deuxième : il vérifie d'abord s'il possède dans sa main la carte complémentaire à celle jouée par le joueur. Si c'est le cas, il vérifie également que cette carte possède une puissance supérieure à celle de son adversaire. Dans ce cas il joue cette carte afin de bénéficier du bonus lié aux cartes complémentaires et de ne subir aucun dégât.

- si il joue en premier ou qu'il ne possède pas de carte complementaire plus puissante : il choisit simplement la carte ayant la puissance d'attaque la plus élevée parmi celles disponibles dans sa main.

Au niveau 3, sur les plateaux moyen et grand, le Dark Magician tient compte de la distance qui le sépare du joueur et de la distance entre le joueur et la sortie du labyrinthe.


## Les structures de données utilisées

| Structure | Utilisation dans le code |
|---|---|
| Liste de listes (`list[list[str]]`) | les plateaux : chaque case est un caractère (`#`, `J`, `M`, `\|`, espace) |
| Dictionnaire (`dict`) | le graphe : une case libre → la liste des cases libres voisines |
| File (`deque`) | la pioche de cartes : on pioche au début et on remet la carte jouée à la fin |
| Liste (`list`) | la main du joueur : 4 cartes visibles |
| Tas binaire (`heapq`) | la file de priorité de A\*, pour traiter d'abord la case la plus prometteuse |
| Dictionnaires | les dégâts et les coûts des cartes et les paires complémentaires de cartes |

## Le graphe du labyrinthe

Le plateau est une grille, mais pour que le Dark Magician puisse le parcourir, on le transforme en **graphe** avec `construire_graphe` :
chaque case libre du plateau devient un **sommet** repéré par ses coordonnées (x,y)

On obtient un dictionnaire de la forme :

```python
graphe = {
    (1, 1): [(2, 1), (1, 2)],
    (2, 1): [(1, 1), (3, 1)],
    # ...
}
```


## L'algorithme A\*

A\* sert à trouver le **plus court chemin** entre la case du Dark Magician et celle du joueur.

Pour chaque case, il utilise trois valeurs  :

- `g(n)` : le nombre de pas **déjà faits** depuis le départ ;
- `h(n)` : une estimation du nombre de pas **restants**, c'est la **distance de Manhattan** :
  `h(n) = |x - x_joueur| + |y - y_joueur|` ;
- `f(n) = g(n) + h(n)` : la **priorité** de la case. Plus `f` est petit, plus la case est prometteuse.

Le dictionnaire `couts` retient le plus petit `g` connu pour chaque case : c'est le **nombre minimal de pas** pour l'atteindre depuis le départ.

Dans le code, `a_star` utilise `heapq` pour la file de priorité.
Elle stocke des triplets (coût estimé, coût réel, position)
- estimation du coup **total** du chemin passant par cette case : 'f=g+h'
- coût déjà payé pour atteindre cette case depuis le départ : 'g'
- position de la case concernée

parents est un dict construit au fur et a mesure  qui retient, pour chaque case visitée, la case par laquelle on est arrivé. Il est utilisé pour reconstruire le chemin du départ à l'arrivée.

### Principe

```text
file de priorité ← (priorité = h(départ), 0, départ)
coût du départ ← 0

tant que la file n'est pas vide :
    sortir la case de plus petite valeur de f (donc de plus grande priorité)
    si c'est la case du joueur :
        reconstruire le chemin avec les parents et le renvoyer

    pour chaque voisin de la case :
        nouveau_coût ← coût de la case + 1
        si ce coût est meilleur que celui déjà connu :
            enregistrer le coût
            noter la case précédente comme un parent
            ajouter le voisin à la file avec priorité = nouveau_coût + h(voisin)
```


`choisir_deplacement` renvoie **la première case après le départ** sur le chemin le plus court vers le joueur. La même méthode permet au Dark Magician de rejoindre une case à défendre près de la sortie.

### Sources
https://www.datacamp.com/tutorial/a-star-algorithm
https://fr.wikipedia.org/wiki/Algorithme_A*

## Heuristique gloutonne pour les cartes

Pour choisir sa carte, le Dark Magician applique deux règles :

1. jouer la **complémentaire** si elle est en main et **strictement plus forte** 
2. sinon, jouer la carte qui inflige le **maximum de dégâts**

C'est une heuristique **gloutonne** : elle choisit l'action qui semble la meilleure **immédiatement**, sans prévoir les coups suivants.

## IA améliorée au niveau 3

*Au niveau 3, sur les plateaux moyen et grand, le Dark Magician tient compte de la distance qui le sépare du joueur et de la distance entre le joueur et la sortie du labyrinthe.*

Deux distances servent à décider :

- la distance entre le **joueur et la sortie** : si elle est petite, le Dark Magician va défendre la sortie
- la distance entre le **joueur et le Dark Magician** : si elle est grande, cela ne sert à rien de poursuivre.

Les seuils dépendent du plateau :

| Plateau | Distance joueur/sortie pour défendre | Distance joueur/Dark Magician pour arrêter la poursuite |
|---|---|---|
| petit | heuristique désactivée | heuristique désactivée |
| moyen | 4 cases ou moins | 8 cases ou plus |
| grand | 6 cases ou moins | 11 cases ou plus |

Le déroulement est alors le suivant :

1. Il se soigne d'abord s'il a moins de 40 PV et au moins 10 lulus.
2. Si le joueur est assez proche de la sortie, le Dark Magician défend la sortie :
   - si le joueur est à 3 cases ou moins de lui, il le poursuit directement 
   - sinon, il rejoint la case juste avant la sortie. S'il occupe déjà cette case, il reste sur place et attaque
3. Sinon, si le joueur est trop loin de lui, il ne le poursuit pas : il reste sur place et attaque pour économiser ses lulus.
4. Sinon, il poursuit le joueur.

S’il reste sur place, le Dark Magician applique les mêmes règles de choix des cartes qu’aux autres niveaux.


Nous avons choisi ces heuristiques pour que le Dark Magician utilise l'action la plus adaptée à la situation. Aux niveaux 1 et 2, le **déplacement est prioritaire** car il peut permettre au Dark Magician de remporter directement la partie. Au niveau 3, il peut aussi rester sur place pour défendre la sortie ou économiser ses lulus. Lorsqu'il ne se déplace pas, il cherche à **maximiser ses dégâts**.

Sur le petit plateau, le Dark Magician continue de viser le joueur lorsqu’il peut se déplacer.



