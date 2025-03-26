# Système de Réservation de Salles

Une application web basée sur Flask pour la gestion des réservations de salles. Ce système permet aux utilisateurs de parcourir les salles disponibles, de demander des réservations et de consulter le statut de leurs réservations. Les administrateurs peuvent gérer les salles et approuver ou rejeter les demandes de réservation.

## Fonctionnalités

- **Authentification des Utilisateurs** : Inscription, connexion et profils utilisateurs
- **Gestion des Salles** : Parcourir, afficher et réserver des salles
- **Système de Réservation** : Demander, suivre et gérer les réservations de salles
- **Tableau de Bord Administrateur** : Gérer les salles et traiter les demandes de réservation
- **Design Réactif** : Fonctionne sur ordinateurs et appareils mobiles

## Technologies Utilisées

- **Backend** : Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Base de Données** : SQLite
- **Frontend** : Tailwind CSS, Daisy UI
- **JavaScript** : JavaScript Vanilla pour les fonctionnalités interactives

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <repository-url>
   cd room-reservation-system
   ```

2. Créer et activer un environnement virtuel :
   ```bash
   python -m venv venv
   # Sur Windows
   venv\Scripts\activate
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Exécuter l’application :
   ```bash
   python run.py
   ```

5. Accéder à l’application à l’adresse `http://localhost:5000`

## Compte Administrateur par Défaut

Lors du premier lancement, le système crée un compte administrateur par défaut :
- **Email** : admin@example.com
- **Mot de passe** : admin123

*Remarque : Modifiez ces identifiants en environnement de production.*

## Structure du Projet

```
room-reservation-system/
├── app/
│   ├── models/          # Modèles de base de données
│   ├── routes/          # Gestion des routes
│   ├── forms/           # Définition des formulaires
│   ├── templates/       # Modèles HTML
│   ├── static/          # Fichiers statiques (CSS, JS)
│   └── __init__.py      # Factory de l’application
├── requirements.txt     # Dépendances du projet
└── run.py              # Point d’entrée de l’application
```

## Utilisation

### Utilisateurs Réguliers

1. S’inscrire ou se connecter
2. Parcourir les salles disponibles
3. Consulter les détails des salles
4. Demander une réservation de salle
5. Vérifier le statut de la réservation dans le profil

### Administrateurs

1. Se connecter avec les identifiants administrateur
2. Accéder au tableau de bord administrateur
3. Gérer les salles (ajout, modification, suppression)
4. Examiner et traiter les demandes de réservation
5. Consulter toutes les réservations du système

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
