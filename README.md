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

1. Téléchargez les données brutes depuis le [site officiel du Ministère de la Culture](https://data.culture.gouv.fr/explore/dataset/festivals-global-festivals-_-pl/information/) au format CSV.

2. Placez le fichier CSV téléchargé dans le dossier `data` du projet.

3. Exécutez le script d'automatisation pour nettoyer et compléter les données :
   ```
   ./automate.sh
   ```
   Ce script va :
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
3.Committez vos changements (`git commit -m 'Ajout de VotreFeature'`)
4. Poussez vers la branche (`git push origin feature/VotreFeature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
