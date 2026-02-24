# TinyLib
Système de gestion de bibliothèque Python, avec base de données SQLite et interface en ligne de commande (CLI).

## Fonctionnalités
- Création et remplissage des livres de la BDD avec l'import des métadonnées via l'API Open Library
- Création du compte utilisateur avec encodage du mot de passe via bcrypt
- Gestion des emprunts

## Utilisation
1. Mettre en place et remplir la base de données : `python db.py`
2. Lancer l'application : `python cli.py`
