# The Dark Magician
The Dark Magician est un jeu qui se joue sur l'interface terminal de l'ordinateur.
C'est un jeu de cartes et de plateau où le but est de vaincre le Dark Magician ou de lui échapper (en sortant du labyrinthe).

## Installation
Il faut avoir Git et Python 3.10 ou une version plus récente. Le jeu utilise uniquement la bibliothèque standard de Python.

```bash
git clone https://github.com/baronflorian/jeu-majeurinfo.git
cd jeu-majeurinfo
```

## Exécution

Depuis le dossier du projet, lance le jeu dans le terminal.

```bash
python jeu.py
```

Si ton système utilise la commande `python3`, lance `python3 jeu.py`.

## Plateformes supportées
Linux, Windows

## Prérequis

Git et Python 3.10 ou une version plus récente. Le jeu utilise uniquement la bibliothèque standard de Python.

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


