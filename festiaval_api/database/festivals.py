from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from .core import DBFestival, NotFoundError

# Les classes de modèles pour l'API
from pydantic import BaseModel

class AdresseBase(BaseModel):
    adresse_postale: str
    code_insee: str
    region: str
    departement: str
    commune: str
    longitude: float
    latitude: float

class CategorieBase(BaseModel):
    discipline_dominante: str
    sous_categorie: str

class PeriodeBase(BaseModel):
    periode: str
    categorie_periode: str

class FestivalBase(BaseModel):
    nom_festival: str
    annee_creation: int
    site_internet: str

class Festival(FestivalBase):
    adresse: AdresseBase
    categorie: CategorieBase
    periode: PeriodeBase

class FestivalCreate(FestivalBase):
    adresse: AdresseBase
    categorie: CategorieBase
    periode: PeriodeBase

class FestivalUpdate(FestivalBase):
    adresse: AdresseBase
    categorie: CategorieBase
    periode: PeriodeBase

# Fonctions pour interagir avec la base de données
def read_db_one_festival(id_festival: int, session: Session) -> DBFestival:
    db_festival = session.query(DBFestival).options(
        joinedload(DBFestival.adresse),
        joinedload(DBFestival.categorie),
        joinedload(DBFestival.periode)
    ).filter(DBFestival.id_festival == id_festival).first()

    if db_festival is None:
        raise NotFoundError(f"Item with id {id_festival} not found.")
    return db_festival

def read_db_festival(session: Session) -> List[DBFestival]:
    db_festivals = session.query(DBFestival).options(
        joinedload(DBFestival.adresse),
        joinedload(DBFestival.categorie),
        joinedload(DBFestival.periode)
    ).limit(5).all()

    if not db_festivals:
        raise NotFoundError("No festivals found in the database.")
    return db_festivals

def generate_id(session: Session) -> int:
    last_id = session.query(DBFestival.id).order_by(DBFestival.id.desc()).first()
    return last_id[0] + 1 if last_id else 1  # Simplification de la génération d'ID

def create_db_festival(festival_data: FestivalCreate, session: Session) -> DBFestival:
    id_festival = generate_id(session)
    
    # Transformation directe en model_dumpionnaire pour la création de l'entité DBFestival
    db_festival = DBFestival(id=id_festival, **festival_data.model_dump())
    
    session.add(db_festival)
    session.commit()
    session.refresh(db_festival)
    return db_festival

def update_db_festival(festival_id: int, festival_data: FestivalUpdate, session: Session) -> DBFestival:
    db_festival = read_db_one_festival(festival_id, session)
    
    # Mise à jour des données à partir du model_dumpionnaire
    update_data = festival_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(db_festival, key) and value is not None:
            setattr(db_festival, key, value)
    
    session.commit()
    session.refresh(db_festival)
    return db_festival

def delete_db_festival(festival_id: int, session: Session) -> None:
    db_festival = read_db_one_festival(festival_id, session)
    
    session.delete(db_festival)
    session.commit()

# Note: Il est important de gérer les relations et les suppressions en cascade via la configuration de SQLAlchemy si nécessaire.
