#!/bin/bash

# Charger les variables d'environnement depuis le fichier .env
source .env

# Vérifier si les variables sont correctement chargées
if [ -z "$DATA_FESTIVAL_SCRIPT" ] || [ -z "$SQL_SCRIPT" ] || [ -z "$INSERTION_SCRIPT" ] || [ -z "$DATABASE_PATH" ]; then
  echo "Une ou plusieurs variables d'environnement sont manquantes dans le fichier .env"
  exit 1
fi

# Exécuter le script Python pour le traitement des données
echo "Exécution du script Python pour le traitement des données..."
python3 "$DATA_FESTIVAL_SCRIPT"

# Vérifier si le script Python s'est exécuté avec succès
if [ $? -ne 0 ]; then
  echo "Erreur lors de l'exécution du script $DATA_FESTIVAL_SCRIPT"
  exit 1
fi

# Exécuter le script SQL pour créer les tables
echo "Exécution du script SQL pour créer les tables..."
sqlite3 "$DATABASE_PATH" < "$SQL_SCRIPT"

# Vérifier si le script SQL s'est exécuté avec succès
if [ $? -ne 0 ]; then
  echo "Erreur lors de l'exécution du script $SQL_SCRIPT"
  exit 1
fi

# Exécuter le script Python pour insérer les données
echo "Exécution du script Python pour insérer les données..."
python3 "$INSERTION_SCRIPT"

# Vérifier si le script Python s'est exécuté avec succès
if [ $? -ne 0 ]; then
  echo "Erreur lors de l'exécution du script $INSERTION_SCRIPT"
  exit 1
fi

echo "Tous les scripts ont été exécutés avec succès."
