# 🎉 API des Festivals 🎭

## 📖 Description

L'API des Festivals est une application FastAPI conçue pour gérer et fournir des informations sur divers festivals. Elle offre une interface RESTful pour créer, lire, mettre à jour et supprimer (CRUD)des données de festivals, ainsi que des fonctionnalités d'authentification pour sécuriser l'accès.

## 🗂️ Structure du projet


### 📁 Fichiers racine

- `main.py` : 🚀 Point d'entrée de l'application. Configure et lance l'API FastAPI.
- `requirements.txt` : 📋 Liste toutes les dépendances Python nécessaires au projet.
- `automate.sh` : 🚀 Script pour automatiser la récupération, le nettoyage et la complétion des données de Festivals, suivi de la création des tables de la base de données et de l'insertion des données.
- `.env` : 🔑 Fichier pour stocker les variables d'environnement.
- `.gitignore` : 📂 Liste des fichiers et dossiers à ignorer lors du commit (comme les fichiers env ou la base de données).

### 📁 Dossier `database_building`

Ce dossier contient les scripts SQL et les données d'insertion pour la base de données.

- `script.sql` : 🛠️ Script SQL pour la création de la structure de la base de données.
- `insertion_data.sql` : 💾 Script SQL pour l'insertion des données initiales.

### 📁 Dossier `data`

- `data_festival.py` : 🎭 Récupère, nettoie, enrichit et sauvegarde les données des festivals, servant de pipeline ETL pour préparer les informations essentielles à notre application.
- `clean_data_festival.csv` : 🧹 Fichier CSV où nous avons stockée les données des festivals nettoyées et complétées.
- Fichiers `.ipynb` : 📊 Notebooks Jupyter sur lesquels nous avons préalablement travaillé pour l'analyse et le nettoyage de données avant d'automatiser le processus en script.

### 📁 Dossier `festival_api`

- `main.py` : 🌟 Fichier principal de l'API FastAPI.
- `models.py` : 🏗️ Définit les modèles de données pour l'API.

#### 📁 Sous-dossier `database`

- `auth_utils.py` : 🔐 Utilitaires pour l'authentification et l'autorisation.
- `db_auth.py` : 🔑 Gestion de l'authentification dans la base de données.
- `db_core.py` : 🧰 Fonctions de base pour interagir avec la base de données.
- `db_festival.py` : 🎪 Fonctions spécifiques pour gérer les données du festival dans la base de données.

#### 📁 Sous-dossier `routers`

- `authentification.py` : 🚪 Gère les routes liées à l'authentification (login, création d'utilisateur).
- `festivals.py` : 🎉 Contient les routes pour la gestion des événements du festival.

### 📁 Dossier `tests`

Contient les tests pour l'API et la base de données.

- `test_authentification.py` : 🧪 Tests pour les fonctionnalités d'authentification.
- `test_db.py` : 🔍 Tests pour les opérations de base de données.

## 🚀 Fonctionnalités

- 🔐 Authentification des utilisateurs
- 📊 Gestion complète des festivals (CRUD)
- 🗺️ Informations géographiques des festivals
- 🎨 Catégorisation des festivals
- 📅 Gestion des périodes de festivals

## 📥 Récupération et traitement des données

 Exécutez le script d'automatisation pour la récuperer, nettoyer et compléter les données :
   ```
   ./automate.sh
   ```
   Ce script va :
   - Récuperer les données brutes depuis l'API du site data.culture.gouv.fr
   - Nettoyer les données brutes
   - Compléter les adresses manquantes via une API de géocodage
   - Préparer les données pour l'importation dans la base de données
   - Importer les données dans la base de données


## 🛠️ Installation

Pour installer ce projet, suivez les étapes suivantes :

1. Clonez ce dépôt sur votre machine locale :
   ```
   git clone https://github.com/ForskyOnly/projet_final_BDD
   ```

2. Naviguez jusqu'au répertoire du projet :
   ```
   cd api-festivals
   ```

3. Créez un environnement virtuel et activez-le :
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

4. Installez les dépendances nécessaires :
   ```
   pip install -r requirements.txt
   ```

## 🖥️ Utilisation

Pour lancer l'API en mode développement :

```
uvicorn festival_api.main:app --reload
```

L'API sera accessible à l'adresse `http://localhost:8000`.

Documentation interactive de l'API : `http://localhost:8000/docs`

## 🧪 Tests

Pour exécuter les tests :

```
python -m pytest
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/VotreFeature`)
3. Committ
4. Poussez vers la branche 
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
