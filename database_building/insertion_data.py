import sqlite3
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def get_periode_id(cur, periode_value):
    """Fonction pour récupérer l'ID de la période donnée"""
    cur.execute("SELECT ID_Periode FROM PERIODE WHERE Periode = ?", (periode_value,))
    row = cur.fetchone()
    if row:
        return row[0] 
    else:
        return None

def get_categorie_id(cur, discipline_dominante, sous_categorie):
    """Fonction pour récupérer l'ID de la catégorie donnée"""
    cur.execute("SELECT ID_Categorie FROM CATEGORIE WHERE Discipline_Dominante = ? AND Sous_Categorie = ?", (discipline_dominante, sous_categorie))
    row = cur.fetchone()
    if row:
        return row[0]  
    else:
        return None

def get_adresse_id(cur, adresse_postale, code_insee):
    """Fonction pour récupérer l'ID de l'adresse donnée"""
    cur.execute("SELECT ID_Adresse FROM ADRESSE WHERE Adresse_Postale = ? AND Code_INSEE = ?", (adresse_postale, code_insee))
    row = cur.fetchone()
    if row:
        return row[0]  
    else:
        return None

# Connexion à la base de données SQLite
chemin_bdd = os.getenv('CHEMIN_BDD')
chemin_csv = os.getenv('CHEMIN_CSV')

conn = sqlite3.connect(chemin_bdd)
cur = conn.cursor()

# Ouvrir le fichier CSV et insérer les données dans la table correspondante
with open(chemin_csv, 'r', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)

    for row in csv_reader:
        # Récupérer l'ID de l'adresse, si elle existe déjà
        adresse_id = get_adresse_id(cur, row['Adresse_Postale'], row['Code_INSEE'])
        
        # Si l'ID de l'adresse n'existe pas, insérer une nouvelle entrée dans la table ADRESSE
        if adresse_id is None:
            cur.execute("INSERT INTO ADRESSE (Adresse_Postale, Code_INSEE, Region, Departement, Commune, Longitude, Latitude) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['Adresse_Postale'], row['Code_INSEE'], row['Region'], row['Departement'], row['Commune'], row['Longitude'], row['Latitude']))
            adresse_id = cur.lastrowid
        
        # Récupérer l'ID de la période, si elle existe déjà
        periode_id = get_periode_id(cur, row['Periode'])
        
        # Si l'ID de la période n'existe pas, insérer une nouvelle entrée dans la table PERIODE
        if periode_id is None:
            cur.execute("INSERT INTO PERIODE (Periode, Categorie_Periode) VALUES (?, ?)", (row['Periode'], row['Categorie_Periode']))
            periode_id = cur.lastrowid
        
        # Récupérer l'ID de la catégorie, si elle existe déjà
        categorie_id = get_categorie_id(cur, row['Discipline_Principale'], row['Sous_Catégorie'])

        # Si l'ID de la catégorie n'existe pas, insérer une nouvelle entrée dans la table CATEGORIE
        if categorie_id is None:
            cur.execute("INSERT INTO CATEGORIE (Discipline_Dominante, Sous_Categorie) VALUES (?, ?)", (row['Discipline_Principale'], row['Sous_Catégorie']))
            categorie_id = cur.lastrowid
        
        # Insertion dans la table FESTIVAL en utilisant les IDs de la période, de la catégorie et de l'adresse
        cur.execute("INSERT INTO FESTIVAL (ID_Periode, ID_Categorie, ID_Adresse, Nom_Festival, Annee_Creation, Site_Internet) VALUES (?, ?, ?, ?, ?, ?)", (periode_id, categorie_id, adresse_id, row['Nom_Festival'], row['Annee_Creation'], row['Site_Internet']))

# Valider (commit) les changements
conn.commit()

# Fermer la connexion à la base de données
conn.close()
