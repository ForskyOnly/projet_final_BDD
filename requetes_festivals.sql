-- Requête 1 : Récupérer tous les festivals créés avant 1970
SELECT f.Nom_Festival, f.Annee_Creation, c.Discipline_Dominante
FROM FESTIVAL f
JOIN CATEGORIE c ON f.ID_Categorie = c.ID_Categorie
WHERE f.Annee_Creation < 1970
ORDER BY f.Annee_Creation DESC;

-- Requête 2 : Compter le nombre de festivals par région
SELECT a.Region, COUNT(*) as Nombre_Festivals
FROM FESTIVAL f
JOIN ADRESSE a ON f.ID_Adresse = a.ID_Adresse
GROUP BY a.Region
ORDER BY Nombre_Festivals DESC;

-- Requête 3 : Trouver les festivals de musique qui se déroulent en été regroupés par région et ville
SELECT f.Nom_Festival, p.Periode, c.Sous_Categorie, a.Commune, a.Region
FROM FESTIVAL f
JOIN PERIODE p ON f.ID_Periode = p.ID_Periode
JOIN CATEGORIE c ON f.ID_Categorie = c.ID_Categorie
JOIN ADRESSE a ON f.ID_Adresse = a.ID_Adresse
WHERE c.Discipline_Dominante = 'Musique'
  AND p.Categorie_Periode = 'Saison'
  AND (p.Periode LIKE '%Juillet%' OR p.Periode LIKE '%Août%');

-- Requête 4 : Récupérer les festivals avec leurs coordonnées géographiques
SELECT f.Nom_Festival, a.Latitude, a.Longitude
FROM FESTIVAL f
JOIN ADRESSE a ON f.ID_Adresse = a.ID_Adresse
WHERE a.Latitude IS NOT NULL AND a.Longitude IS NOT NULL;

-- Requête 5 : Trouver les festivals les plus anciens par catégorie
SELECT c.Discipline_Dominante, f.Nom_Festival, f.Annee_Creation
FROM FESTIVAL f
JOIN CATEGORIE c ON f.ID_Categorie = c.ID_Categorie
WHERE (c.Discipline_Dominante, f.Annee_Creation) IN (
    SELECT c2.Discipline_Dominante, MIN(f2.Annee_Creation)
    FROM FESTIVAL f2
    JOIN CATEGORIE c2 ON f2.ID_Categorie = c2.ID_Categorie
    GROUP BY c2.Discipline_Dominante
)
ORDER BY f.Annee_Creation;


