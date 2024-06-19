import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json
import re
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def charger_variables_env():
    """
    Charge les variables d'environnement à partir d'un fichier .env.

    Cette fonction charge les variables d'environnement en utilisant le module dotenv
    et retourne la valeur de la clé API spécifiée dans le fichier .env.

    Return :
    --------
    str
        La clé API extraite des variables d'environnement, ou None si la clé n'est pas trouvée.
    """
    load_dotenv()

    logging.info("Variables d'environnement chargées.")
    return os.getenv("API_KEY")



def recuperer_donnees_api(dataset_id, api_key):
    """
    Récupère les données depuis l'API donnée en utilisant le dataset_id et la clé API.

    Cette fonction envoie une requête HTTP GET à l'API en utilisant l'identifiant
    du dataset et la clé API fournie. Elle tente de récupérer les données sous
    forme de JSON et les retourne. En cas d'erreur, elle affiche un message d'erreur
    approprié.

    Params :
    --------
    dataset_id : str
        L'identifiant du dataset à récupérer.
    api_key : str
        La clé API pour l'accès aux données.

    Return :
    --------
    list ou None
        Les données récupérées sous forme de liste de dictionnaires, ou None en cas d'échec.
    """
    url = f"https://data.culture.gouv.fr/api/v2/catalog/datasets/{dataset_id}/exports/json"
    headers = {'X-API-KEY': api_key}
    logging.info(f"Envoi de la requête à l'API pour le dataset {dataset_id}.")
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            logging.info("Données récupérées avec succès.")
            return response.json()
        except json.JSONDecodeError as e:
            logging.error("Erreur de décodage JSON:", e)
            return None
    else:
        logging.error(f"Échec de la requête. Code d'état: {response.status_code}")
        return None


def extraire_annee(annee_str):
    """
    Extrait une année à partir d'une chaîne de caractères.

    Cette fonction trouve et retourner une année à partir d'une chaîne
    de caractères en utilisant plusieurs expressions régulières pour différents formats
    d'année.

    Params :
    --------
    annee_str : str
        La chaîne de caractères contenant l'année potentielle.

    Return :
    --------
    int ou None
        L'année extraite sous forme d'entier, ou None si aucune année n'a pu être trouvée.
    """
    if pd.isnull(annee_str):
        return None
    
    annee_str = str(annee_str)
    # Trouver une année à 4 chiffres (e.g., 2021)
    match = re.search(r'\b(19|20)\d{2}\b', annee_str)
    if match:
        return int(match.group(0))
    
    # Trouver une année à 4 chiffres même si elle est suivie par d'autres caractères (ex: 2021a) group(0) : Retourne l'intégralité de la correspondance trouvée par le regex
    match = re.search(r'\b(19|20)\d{2}', annee_str)
    if match:
        return int(match.group(0))
    
    # Trouver une année à 2 chiffres avec le format ex: "12ème en 21" et calculer l'année (ex : 12ème en 21 -> 2021 -12 = 2009) 2021 car le jeu de donnée est datée de 2021
    match = re.search(r'(\d{1,2})\D*en\s(\d{2})', annee_str)
    if match:
        return 2021 - int(match.group(1))
    
    # Trouver des années au format "XXème" et calculer l'année (ex: 12ème -> 2009) group(1) : Retourne les chaînes correspondant aux groupes capturés par les parenthèses dans le regex
    match = re.search(r'(\d{1,2})\D*ème', annee_str)
    if match:
        return 2021 - int(match.group(1))
    
    # Trouver des années au format "17ans" et calculer l'année (ex: 17ans -> 2004)
    match = re.search(r'(\d{1,2})\s?ans', annee_str)
    if match:
        return 2021 - int(match.group(1))
    
    # Trouver des années séparées par des slashs et conserver la première année (ex: 2021 / 2022 -> 2021)
    match = re.search(r'(\d{4})\s?/\s?(\d{4})', annee_str)
    if match:
        return int(match.group(1))
    return None


def uniformiser_sous_categorie(value):
    """
    Nettoie la valeur de la sous-catégorie en supprimant les numéros suivis d'un tiret et d'un espace,
    et en remplaçant les valeurs vides par 'Inconnu'.

    Params :
    --------
    value : str
        La chaîne de caractères représentant la sous-catégorie à nettoyer.

    Return :
    --------
    str
        La chaîne de caractères nettoyée.
    """
    # Supprimer les numéros suivis d'un tiret et d'un espace (ex: "123 - ")
    value = re.sub(r'\d+\s*-\s*', '', value)
    value = value.strip()

    if not value:
        return 'Inconnu'
    return value


def categoriser_periode(periode):
    """
    Catégorise une période en fonction de son contenu.

    Cette fonction prend une chaîne de caractères représentant une période et
    retourne une catégorie basée sur des mots-clés spécifiques et des mois inclus
    dans la chaîne.

    Params :
    --------
    periode : str
        La chaîne de caractères représentant la période à catégoriser.

    Return :
    --------
    str
        La catégorie de la période.
    """
    if pd.isna(periode):
        return "Inconnu"
    
    periode = periode.lower()  

    if 'avant-saison' in periode:
        return 'Avant-saison'
    elif any(mois in periode for mois in ['janvier', 'février', 'mars', 'avril', 'mai']):
        return 'Avant-saison'
    elif 'saison' in periode:
        return 'Saison'
    elif any(mois in periode for mois in ['juin', 'juillet', 'août', 'septembre']):
        return 'Saison' 
    elif 'après-saison' in periode:
        return 'Après-saison'
    elif any(mois in periode for mois in ['octobre', 'novembre', 'décembre']):
        return 'Après-saison'
    elif 'janvier, février, mars, avril, mai, juin, juillet, août' in periode:
        return 'Période Variable'
    else:
        return 'Période Variable'
    
    
def uniformiser_periode(period):
    """
    Uniformise la chaîne de caractères représentant une période en mettant en majuscule la première lettre de chaque mot,
    en supprimant les termes spécifiques et les parenthèses.

    Params :
    --------
    period : str
        La chaîne de caractères représentant la période à uniformiser.

    Return :
    --------
    str
        La chaîne de caractères uniformisée.
    """
    if period is None:
        return None
    
    period = ' '.join(word.capitalize() for word in period.split())
    period = period.replace('Avant-saison', '').replace('Saison', '').replace('Après-saison', '').replace('(', '').replace(')', '')
    
    return period.strip()


def gen_adresse_depuis_coordonnees(lat, lon):
    """
    Récupère une adresse complète à partir de coordonnées de latitude et de longitude en utilisant l'API Nominatim d'OpenStreetMap.

    Params :
    --------
    lat : float
        La latitude des coordonnées.
    lon : float
        La longitude des coordonnées.

    Return :
    --------
    str
        L'adresse complète sous forme de chaîne de caractères. Retourne une chaîne vide en cas d'erreur ou si l'adresse n'est pas trouvée.
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        
        # Pause pour éviter de surcharger l'API (l'API est gratuite mais a des limites de fréquence de 1seconde par requête)
        time.sleep(1)
        
        response = requests.get(url)
        if response.status_code == 200:
            logging.info("Adresses récupérées avec succès.")
            json_data = response.json()
            
            if "address" in json_data:
                address = json_data["address"]
                
                # Construire l'adresse complète depuis les données de l'API
                full_address = ", ".join(filter(None, [
                    address.get("road", ""),           # Nom de la rue
                    address.get("quarter", ""),        # Quartier
                    address.get("city", ""),           # Ville
                    address.get("municipality", ""),   # Municipalité
                    address.get("county", ""),         # Comté
                    address.get("state", ""),          # État
                    address.get("region", ""),         # Région
                    address.get("postcode", "")        # Code postal
                ]))
                
                return full_address
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'adresse : {e}")
    return ""


def renommer_et_creer_colonnes(df):
    """
    Renomme les colonnes du DataFrame et crée de nouvelles colonnes combinées.

    Cette fonction renomme les colonnes existantes du DataFrame selon un
    mapping prédéfini, remplit les colonnes de sous-catégorie avec des
    valeurs vides par des chaînes vides et les combine en une seule colonne
    'Sous_Categorie'. Elle retourne ensuite un DataFrame avec une sélection
    spécifique de colonnes.

    Params :
    --------
    df : pandas.DataFrame
        Le DataFrame contenant les données initiales.

    Return :
    --------
    pandas.DataFrame
        Le DataFrame avec les colonnes renommées et la nouvelle colonne 'Sous_Categorie'.
    """
    df_renomme = df.rename(columns={
        'nom_du_festival': 'Nom_Festival',
        'region_principale_de_deroulement': 'Region',
        'departement_principal_de_deroulement': 'Departement',
        'commune_principale_de_deroulement': 'Commune',
        'code_insee_commune': 'Code_INSEE',
        'site_internet_du_festival': 'Site_Internet',
        'annee_de_creation_du_festival': 'Annee_Creation',
        'discipline_dominante': 'Discipline_Principale',
        'periode_principale_de_deroulement_du_festival': 'Periode',
        'geocodage_xy': 'Geocode'
    })
    
    colonnes_sous_categorie = [
        'sous_categorie_spectacle_vivant', 'sous_categorie_musique',
        'sous_categorie_musique_cnm', 'sous_categorie_cinema_et_audiovisuel',
        'sous_categorie_arts_visuels_et_arts_numeriques',
        'sous_categorie_livre_et_litterature'
    ]

    df_renomme[colonnes_sous_categorie] = df_renomme[colonnes_sous_categorie].fillna('').astype(str)
    df_renomme['Sous_Categorie'] = df_renomme[colonnes_sous_categorie].agg(' '.join, axis=1)
    
    colonnes_selectionnees = [
        'Nom_Festival', 'Region', 'Departement', 'Commune', 
        'Code_INSEE', 'Annee_Creation', 'Discipline_Principale', 
        'Sous_Categorie', 'Periode', 'Geocode'
    ]

    return df_renomme[colonnes_selectionnees]



def nettoyer_donnees(df):
    """
    Nettoie et transforme les données du DataFrame.

    Cette fonction effectue plusieurs opérations de nettoyage et de transformation
    sur les données du DataFrame. Elle extrait les coordonnées géographiques,
    normalise les sous-catégories, catégorise les périodes, uniformise les périodes,
    et génère des adresses complètes à partir des coordonnées.

    Params :
    --------
    df : pandas.DataFrame
        Le DataFrame contenant les données initiales à nettoyer.

    Return :
    --------
    pandas.DataFrame
        Le DataFrame nettoyé et transformé.
    """
    logging.info("Nettoyage des données en cours.")
    # extraire uniquement la coordonnée de latitude depuis le format {'lat': 44.773185218} dans une nouvelle colonne Latitude
    df['Latitude'] = df['Geocode'].apply(lambda x: x['lat'] if x is not None else None)
    # extraire uniquement la coordonnée delongitude depuis le format {'lon':  -0.558212256384} dans une nouvelle colonne Longitude
    df['Longitude'] = df['Geocode'].apply(lambda x: x['lon'] if x is not None else None)

    df['Annee_Creation'] = df['Annee_Creation'].apply(extraire_annee).astype('Int64')
    df['Sous_Categorie'] = df['Sous_Categorie'].apply(uniformiser_sous_categorie)
    df['Categorie_Periode'] = df['Periode'].apply(categoriser_periode)
    df['Periode'] = df['Periode'].apply(uniformiser_periode)

    logging.info("1ere partie de nettoyage des données terminé.")
    logging.info("Debut de la récuperaion des adresses avec les coordonnées.")

    df['Adresse_Complete'] = df.apply(lambda row: gen_adresse_depuis_coordonnees(row['Latitude'], row['Longitude']) if not pd.isna(row['Latitude']) and not pd.isna(row['Longitude']) else "", axis=1)
    logging.info("Adresse récupérée avec succès.") # Si l'adresse est récupérée avec succès, pour chaque ligne du DF le message s'affiche 

    df = df.drop(columns=['Geocode'], axis=1)
    
    logging.info("Récuperation des adresses términé.")
    logging.info("Nettoyage des données terminé.")
    return df


def sauvegarder_en_csv(df, nom_fichier):
    """
    Sauvegarde le DataFrame dans un fichier CSV.

    Cette fonction prend un DataFrame en entrée et le sauvegarde dans un fichier CSV
    avec le nom de fichier spécifié.

    Params :
    --------
    df : pandas.DataFrame
        Le DataFrame à sauvegarder.
    nom_fichier : str
        Le nom du fichier CSV où les données seront sauvegardées.

    Return :
    --------
    None
    """
    df.to_csv(nom_fichier, index=False)
    logging.info(f"Les données ont été sauvegardées dans {nom_fichier}.")


def main():
    """
    Exécute le script principal pour récupérer, nettoyer et sauvegarder les données du festival.

    Cette fonction charge les variables d'environnement pour obtenir la clé API,
    utilise cette clé pour récupérer les données du dataset spécifié via l'API,
    nettoie et transforme ces données, puis les sauvegarde dans un fichier CSV.

    Params :
    --------
    None

    Return :
    --------
    None
    """
    logging.info("Début de l'exécution du script.")
    api_key = charger_variables_env()
    dataset_id = "festivals-global-festivals-_-pl"
    
    donnees = recuperer_donnees_api(dataset_id, api_key)
    if donnees is not None:
        df = pd.DataFrame(donnees)
        df_renomme = renommer_et_creer_colonnes(df)
        df_nettoye = nettoyer_donnees(df_renomme)
        sauvegarder_en_csv(df_nettoye, 'clean_festival_data.csv')
    logging.info("Fin de l'exécution du script.")

if __name__ == "__main__":
    main()