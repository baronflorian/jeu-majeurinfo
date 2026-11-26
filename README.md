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
├── joueur.py      # Joueur humain et Dark Magician
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


