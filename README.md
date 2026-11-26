# The Dark Magician
The Dark Magician est un jeu qui se joue sur l'interface terminal de l'ordinateur.
C'est un jeu de cartes et de plateau où le but est de vaincre le Dark Magician ou de lui échapper (en sortant du labyrinthe).

## Installation
```bash
git clone https://github.com/baronflorian/jeu-majeuroinfo
mettre des instructions jsp moi

```

## Exécution
```bash
python jeu.py         # ou : pipenv run python jeu.py
```

## Plateformes supportées
Linux, Windows

## Prérequis
Python 3.10+
(utilisation de collections et heapq)

## Commandes du jeu
- z/s/q/d déplacement
- a attaquer
- s soigner
- q quitter
- Entrée passer/continuer

## Structure du projet
projet/
├── valeur.py      # données du jeu
├── player.py      # classe de base commune
├── joueur.py      # Joueur (humain) + Ordi (dark magician)
├── parcours.py    # graphe, A*, déplacements
├── attaque.py     # résolution des attaques
├── jeu.py         # boucle principale et interface texte
├── README.md
├── GAME.md
└── ALGORITHMS.md

## Auteurs
Lucie Fontanini
Florian Baron
Julie Bruel


# Magicien
## Règles du jeu

Le joueur J gagne s'il atteint la sortie | ou s'il bat le Dark Magician M avec ses attaques. 
On ne peut pas passer par dessus le Dark Magician.

Le joueur perd si le Dark Magician arrive sur sa case ou si ses attaques lui font perdre tous ses PV.

Si le Dark magician lance une action complémentaire à notre attaque,
un seul prend les dégats de pv : la difference des dégats des deux attaques + 2.
    
On peut sélectionner à chaque tour une carte parmis quatre cartes parmis les 8 du jeux.
Il est donc impossible de réutiliser deux fois d'affilé la même carte.
Le joueur dépense 2 lulus pour jouer Foudre ou Terre et 4 lulus pour jouer Magie ou Temps. Les autres cartes du joueur sont gratuites.

Si aucune carte en main n'est jouable, le joueur passe son tour et reçoit une carte gratuite en remplacement à la fin du tour.

Le joueur utilise la même réserve de lulus pour jouer ses cartes, se déplacer et se soigner. Il peut se soigner une fois par tour, avant ou après son attaque ou son déplacement.
Le joueur d'après lancera une attaque sans toucher l'adversaire, sauf si il se déplace.
Toute attaque est comptabilisée si et seulement si le joueur précedent n'a pas bougé.
