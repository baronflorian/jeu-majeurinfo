# Heuristique de choix des actions du Dark Magicien:
*Le Dark Magicien suit une stratégie basée sur des règles de priorité afin de choisir l'action qui lui semble la plus avantageuse.*

si le dark magicien a moin de 10 pv il va se soigner en priorité afin de ne pas perdre la partie 

Si il n'a pas besoin de se soigner le Dark Magicien cherche en priorité à se déplacer lorsqu'il en a la possibilité. Ce choix lui permet de se rapprocher du joueur et de tenter de l'atteindre afin de remporter la partie.

Si le déplacement n'est pas possible, le Dark Magicien cherche à infliger le maximum de dégâts au joueur.

Pour cela, son choix dépend de l'ordre de jeu :
- S'il joue en deuxième : il vérifie d'abord s'il possède dans sa main la carte complémentaire à celle jouée par le joueur. Si c'est le cas, il vérifie également que cette carte possède une puissance supérieure à celle de son adversaire. Dans ce cas il joue cette carte afin de bénéficier du bonus lié aux cartes complémentaires et de ne subir aucun dégât.

- si il joue en premier ou qu'il ne possède pas de carte complementaire plus puissante : il choisit simplement la carte ayant la puissance d'attaque la plus élevée parmi celles disponibles dans sa main.

Au niveau 3, le Dark Magicien adopte une stratégie plus élaborée. Contrairement aux niveaux précédents, il ne cherche plus systématiquement à se déplacer dès que cela est possible. Il analyse désormais la position du joueur par rapport à la sienne, mais également la distance qui sépare le joueur de la sortie du labyrinthe.

Son objectif de déplacement peut ainsi évoluer selon trois situations :

Le joueur est trop éloigné : le Dark Magicien préfère rester sur place et attendre que le joueur se rapproche. Cela lui permet d'économiser ses lulus plutôt que de dépenser des ressources pour parcourir inutilement le labyrinthe. Il peut ainsi conserver ses ressources pour ses attaques.

Le joueur se rapproche dangereusement de la sortie : le Dark Magicien change de stratégie et se dirige vers la sortie afin de la défendre et d'empêcher le joueur de gagner en s'échappant du labyrinthe.

Le joueur se rapproche trop du Dark Magicien : celui-ci abandonne temporairement la défense de la sortie pour se concentrer à nouveau sur la poursuite du joueur. Il cherche ainsi à ne pas laisser le joueur s'échapper et à tenter de l'éliminer directement.

Lorsque le déplacement ou le soin ne sont pas prioritaires, le Dark Magicien conserve sa stratégie de choix des cartes : il cherche à profiter des cartes complémentaires lorsqu'elles sont avantageuses et, dans les autres cas, joue la carte qui inflige le plus de dégâts.



Ces heuristiques ont été choisies pour privilégier les actions les plus avantageuses. Le **déplacement est prioritaire** car il peut permettre au Dark Magicien de remporter directement la partie. Lorsqu'il ne peut pas se déplacer, il cherche à **maximiser ses dégâts**.

Au niveau 3, l'IA continue de privilégier les actions les plus avantageuse mais elle ne se contente plus de prioritiser le déplacement et de maximiser les dégats elle prend en compte différents éléments stratégiques. Ces choix permettent d'obtenir une IA plus réactive, capable de changer d'objectif en fonction de l'évolution de la partie. Elle cherche ainsi à équilibrer trois objectifs : économiser ses ressources, empêcher le joueur de s'échapper et éviter d'être vaincue.


## Les structures de données utilisées

| Structure | Utilisation dans le code |
|---|---|
| Liste de listes (`list[list[str]]`) | les plateaux : chaque case est un caractère (`#`, `J`, `M`, `/`, espace) |
| Dictionnaire (`dict`) | le graphe : une case libre → la liste des cases libres voisines |
| File (`deque`) | la pioche de cartes : on pioche au début et on remet la carte jouée à la fin |
| Liste (`list`) | la main du joueur : 4 cartes visibles |
| Tas binaire (`heapq`) | la file de priorité de A\*, pour traiter d'abord la case la plus prometteuse |
| Dictionnaires | les dégâts et les coûts des cartes et les paires complémentaires de cartes |

## Le graphe du labyrinthe

Le plateau est une grille, mais pour que l'IA puisse le parcourir, on le transforme en **graphe** avec `construire_graphe` :
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


`choisir_deplacement` récupère ce chemin et renvoie **la première case après le départ** : le Dark Magician avance ainsi d'une case par tour vers le joueur.

### Sources
https://www.datacamp.com/tutorial/a-star-algorithm
https://fr.wikipedia.org/wiki/Algorithme_A*

## Heuristique gloutonne pour les cartes

Pour le choix de la carte, l'IA ne simule pas toute la partie : elle applique deux règles :

1. jouer la **complémentaire** si elle est en main et **strictement plus forte** 
2. sinon, jouer la carte qui inflige le **maximum de dégâts**

C'est une heuristique **gloutonne** : elle choisit l'action qui semble la meilleure **immédiatement**, sans prévoir les coups suivants.


