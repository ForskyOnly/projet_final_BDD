from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from .core import DBFestival, DBAdresse, DBPeriode, DBCategorie, NotFoundError

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
    last_id = session.query(DBFestival.id_festival).order_by(DBFestival.id_festival.desc()).first()
    return last_id[0] + 1 if last_id else 1  

def create_db_festival(festival_data: FestivalCreate, session: Session) -> DBFestival:
    id_festival = generate_id(session)
    
    # Créer les instances des relations à partir des données fournies
    adresse = DBAdresse(**festival_data.adresse.model_dump())
    categorie = DBCategorie(**festival_data.categorie.model_dump())
    periode = DBPeriode(**festival_data.periode.model_dump())
    
    # Créer l'instance du festival avec ses relations
    db_festival = DBFestival(
        id_festival=id_festival,
        nom_festival=festival_data.nom_festival,
        annee_creation=festival_data.annee_creation,
        site_internet=festival_data.site_internet,
        adresse=adresse,
        categorie=categorie,
        periode=periode
    )
    
    session.add(db_festival)
    session.commit()
    session.refresh(db_festival)
    
    return db_festival

def update_db_festival(festival_id: int, festival_data: FestivalUpdate, session: Session) -> DBFestival:
    db_festival = session.query(DBFestival).get(festival_id)
    if not db_festival:
        raise NotFoundError(f"Festival with id {festival_id} not found.")

    # Mise à jour des champs simples
    if festival_data.nom_festival is not None:
        db_festival.nom_festival = festival_data.nom_festival
    if festival_data.annee_creation is not None:
        db_festival.annee_creation = festival_data.annee_creation
    if festival_data.site_internet is not None:
        db_festival.site_internet = festival_data.site_internet

    # Mise à jour de l'adresse
    if festival_data.adresse:
        if db_festival.adresse:
            for key, value in festival_data.adresse.model_dump(exclude_none=True).items():
                setattr(db_festival.adresse, key, value)
        else:
            db_festival.adresse = DBAdresse(**festival_data.adresse.model_dump())

    # Mise à jour de la catégorie
    if festival_data.categorie:
        if db_festival.categorie:
            for key, value in festival_data.categorie.model_dump(exclude_none=True).items():
                setattr(db_festival.categorie, key, value)
        else:
            db_festival.categorie = DBCategorie(**festival_data.categorie.model_dump())

    # Mise à jour de la période
    if festival_data.periode:
        if db_festival.periode:
            for key, value in festival_data.periode.model_dump(exclude_none=True).items():
                setattr(db_festival.periode, key, value)
        else:
            db_festival.periode = DBPeriode(**festival_data.periode.model_dump())

    session.commit()
    session.refresh(db_festival)
    return db_festival

def delete_db_festival(festival_id: int, db: Session) -> bool:
    db_festival = db.query(DBFestival).filter(DBFestival.id_festival == festival_id).first()
    if db_festival is None:
        return False  # Le festival n'existe pas, donc la suppression n'a pas eu lieu
    db.delete(db_festival)
    db.commit()
    return True  # Le festival a été supprimé avec succès

# Note: Il est important de gérer les relations et les suppressions en cascade via la configuration de SQLAlchemy si nécessaire.
