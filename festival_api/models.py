from pydantic import BaseModel
from typing import Optional

class AdresseBase(BaseModel):
    adresse_postale: str
    code_insee: str
    region: str
    departement: str
    commune: str
    longitude: float
    latitude: float

class AdresseCreate(AdresseBase):
    pass

class AdresseResponse(AdresseBase):
    id: int

    class Config:
        from_attributes = True

class CategorieBase(BaseModel):
    discipline_dominante: str
    sous_categorie: str

class CategorieCreate(CategorieBase):
    pass

class CategorieResponse(CategorieBase):
    id: int

    class Config:
        from_attributes = True

class PeriodeBase(BaseModel):
    periode: str
    categorie_periode: str

class PeriodeCreate(PeriodeBase):
    pass

class PeriodeResponse(PeriodeBase):
    id: int

    class Config:
        from_attributes = True

class FestivalBase(BaseModel):
    id_periode: int
    id_categorie: int
    id_adresse: int
    nom_festival: str
    annee_creation: int
    site_internet: Optional[str]

class FestivalCreate(FestivalBase):
    pass

class FestivalResponse(FestivalBase):
    id: int

    class Config:
        from_attributes = True