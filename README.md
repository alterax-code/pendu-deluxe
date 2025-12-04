# 🎮 Pendu Deluxe

Un jeu du pendu moderne avec une interface graphique Pygame et des effets visuels avancés.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Fonctionnalités

- Interface graphique moderne avec dégradés et animations
- Lettres animées tombantes en arrière-plan
- Système de particules pour les effets visuels
- Bonhomme pendu animé avec expressions faciales
- Système d'indices (révèle des lettres contre des pénalités)
- Barre de progression des erreurs avec indicateur coloré
- Catégories de mots variées (animaux, pays, couleurs, sports, fruits)
- Options de volume et son
- Effets sonores

## 🖼️ Aperçu

Le jeu propose une fenêtre de 1000x700 pixels avec :
- Un fond dégradé animé
- Des lettres qui tombent en arrière-plan
- Un clavier virtuel coloré
- Un panneau d'informations avec barre de progression

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- Pygame 2.0 ou supérieur

### Étapes

1. Clonez le repository :
```bash
git clone https://github.com/VOTRE_USERNAME/pendu-deluxe.git
cd pendu-deluxe
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez le jeu :
```bash
python hangman.py
```

## 🎯 Comment jouer

| Touche | Action |
|--------|--------|
| `A-Z` | Deviner une lettre |
| `F4` | Obtenir un indice (+5 pénalités) |
| `F5` | Nouvelle partie |
| `F6` | Options (volume, son) |
| `ESC` | Quitter |

### Règles

- Devinez le mot caché lettre par lettre
- Chaque mauvaise lettre ajoute une partie au pendu
- Vous avez droit à 10 erreurs maximum
- Les indices révèlent 1-2 lettres mais coûtent 5 pénalités

## 📁 Structure du projet

```
pendu-deluxe/
├── hangman.py          # Code source principal
├── highscore.json      # Sauvegarde des scores
├── requirements.txt    # Dépendances Python
├── README.md           # Documentation
├── LICENSE             # Licence MIT
└── assets/
    └── myinstants.mp3  # Sons du jeu
```

## 🛠️ Technologies utilisées

- **Python 3** - Langage de programmation
- **Pygame** - Bibliothèque de développement de jeux 2D

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

Développé dans le cadre d'un exercice de formation EPITECH.

---

⭐ N'hésitez pas à mettre une étoile si vous aimez ce projet !
