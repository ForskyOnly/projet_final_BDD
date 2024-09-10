# 🎉 API des Festivals 🎭

## 📖 Description

L'API des Festivals est une application FastAPI robuste conçue pour gérer et fournir des informations sur divers festivals. Elle offre une interface RESTful pour créer, lire, mettre à jour et supprimer des données de festivals, ainsi que des fonctionnalités d'authentification pour sécuriser l'accès.

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
   git clone https://github.com/ForslyONly/api-festivals.git
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