from pydantic import BaseModel
from typing import Optional

class Adresse(BaseModel):
    id: Optional[int]
    adresse_postale: str
    code_insee: str
    region: str
    departement: str
    commune: str
    longitude: float
    latitude: float

    class Config:
        from_attributes = True

class Categorie(BaseModel):
    id: Optional[int]
    discipline_dominante: str
    sous_categorie: str

    class Config:
        from_attributes = True

class Periode(BaseModel):
    id: Optional[int]
    periode: str
    categorie_periode: str

    class Config:
        from_attributes = True

class Festival(BaseModel):
    id: Optional[int]
    id_periode: int
    id_categorie: int
    id_adresse: int
    nom_festival: str
    annee_creation: int
    site_internet: Optional[str]

    class Config:
        from_attributes = True
