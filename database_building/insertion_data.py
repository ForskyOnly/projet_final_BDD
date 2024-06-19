import sqlite3
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def get_periode_id(cur, periode_value):
    """
    Récupère l'ID de la période donnée à partir de la base de données.

    Args:
        cur (sqlite3.Cursor): Le curseur de la base de données.
        periode_value (str): La valeur de la période à rechercher.

    Returns:
        int: L'ID de la période si elle existe, sinon None.
    """
    cur.execute("SELECT ID_Periode FROM PERIODE WHERE Periode = ?", (periode_value,))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None

def get_categorie_id(cur, discipline_dominante, sous_categorie):
    """
    Récupère l'ID de la catégorie donnée à partir de la base de données.

    Args:
        cur (sqlite3.Cursor): Le curseur de la base de données.
        discipline_dominante (str): La discipline dominante à rechercher.
        sous_categorie (str): La sous-catégorie à rechercher.

    Returns:
        int: L'ID de la catégorie si elle existe, sinon None.
    """
    cur.execute("SELECT ID_Categorie FROM CATEGORIE WHERE Discipline_Dominante = ? AND Sous_Categorie = ?", (discipline_dominante, sous_categorie))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None

def get_adresse_id(cur, adresse_postale, code_insee):
    """
    Récupère l'ID de l'adresse donnée à partir de la base de données.

    Args:
        cur (sqlite3.Cursor): Le curseur de la base de données.
        adresse_postale (str): L'adresse postale à rechercher.
        code_insee (str): Le code INSEE à rechercher.

    Returns:
        int: L'ID de l'adresse si elle existe, sinon None.
    """
    cur.execute("SELECT ID_Adresse FROM ADRESSE WHERE Adresse_Postale = ? AND Code_INSEE = ?", (adresse_postale, code_insee))
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        return None

def main():
    """
    Exécute le script principal pour insérer des données de festivals dans une base de données SQLite.

    Cette fonction lit les variables d'environnement pour obtenir les chemins vers la base de données
    et le fichier CSV, puis insère les données du CSV dans la base de données en vérifiant et en
    insérant les entrées nécessaires dans les tables associées.

    Returns:
        None
    """
    chemin_bdd = os.getenv('CHEMIN_BDD')
    chemin_csv = os.getenv('CHEMIN_CSV')

    conn = sqlite3.connect(chemin_bdd)
    cur = conn.cursor()

    with open(chemin_csv, 'r', encoding='utf-8') as csvfile:
        print("Début de l'insertion des données dans la base de données")
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            adresse_id = get_adresse_id(cur, row['Adresse_Postale'], row['Code_INSEE'])

            if adresse_id is None:
                cur.execute("INSERT INTO ADRESSE (Adresse_Postale, Code_INSEE, Region, Departement, Commune, Longitude, Latitude) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['Adresse_Postale'], row['Code_INSEE'], row['Region'], row['Departement'], row['Commune'], row['Longitude'], row['Latitude']))
                adresse_id = cur.lastrowid

            periode_id = get_periode_id(cur, row['Periode'])
            if periode_id is None:
                cur.execute("INSERT INTO PERIODE (Periode, Categorie_Periode) VALUES (?, ?)", (row['Periode'], row['Categorie_Periode']))
                periode_id = cur.lastrowid

            categorie_id = get_categorie_id(cur, row['Discipline_Principale'], row['Sous_Categorie'])
            if categorie_id is None:
                cur.execute("INSERT INTO CATEGORIE (Discipline_Dominante, Sous_Categorie) VALUES (?, ?)", (row['Discipline_Principale'], row['Sous_Categorie']))
                categorie_id = cur.lastrowid

            cur.execute("INSERT INTO FESTIVAL (ID_Periode, ID_Categorie, ID_Adresse, Nom_Festival, Annee_Creation, Site_Internet) VALUES (?, ?, ?, ?, ?, ?)", (periode_id, categorie_id, adresse_id, row['Nom_Festival'], row['Annee_Creation'], row['Site_Internet']))
        print("Données insérées avec succès dans la base de données")

    conn.commit()

    conn.close()

if __name__ == "__main__":
    main()
