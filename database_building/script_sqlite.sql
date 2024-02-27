-- Script SQL pour créer une base de données SQLite pour le schéma de festival

-- Création de la table PERIODE
CREATE TABLE IF NOT EXISTS PERIODE (
    ID_Periode INTEGER PRIMARY KEY AUTOINCREMENT,
    Periode TEXT    ,
    Categorie_Periode TEXT
);

-- Création de la table CATEGORIE
CREATE TABLE IF NOT EXISTS CATEGORIE (
    ID_Categorie INTEGER PRIMARY KEY AUTOINCREMENT,
    Discipline_Dominante TEXT,
    Sous_Categorie TEXT
);

-- Création de la table ADRESSE
CREATE TABLE IF NOT EXISTS ADRESSE (
    ID_Adresse INTEGER PRIMARY KEY AUTOINCREMENT,
    Adresse_Postale TEXT,
    Code_INSEE TEXT,
    Region TEXT,
    Departement TEXT,
    Commune TEXT,
    Longitude REAL,
    Latitude REAL
);

-- Création de la table FESTIVAL
CREATE TABLE IF NOT EXISTS FESTIVAL (
    ID_Festival INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Periode INTEGER,
    ID_Categorie INTEGER,
    ID_Adresse INTEGER,
    Nom_Festival TEXT NOT NULL,
    Annee_Creation INTEGER,
    Site_Internet TEXT,
    FOREIGN KEY (ID_Periode) REFERENCES PERIODE(ID_Periode),
    FOREIGN KEY (ID_Categorie) REFERENCES CATEGORIE(ID_Categorie),
    FOREIGN KEY (ID_Adresse) REFERENCES ADRESSE(ID_Adresse)
);


