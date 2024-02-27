from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .core import DBFestival, NotFoundError

class FestivalBase(BaseModel):
    nom_festival: str
    region: str
    departement: str
    commune: str
    code_insee: str
    site_internet: str
    annee_creation: int
    discipline_principale: str
    sous_categorie: str
    periode: str
    longitude: float
    latitude: float
    categorie_periode: str
    adresse_postale: str

class FestivalCreate(FestivalBase):
    pass

class FestivalUpdate(FestivalBase):
    pass

class Festival(FestivalBase):
    id_festival: int 

    class Config:
        from_attributes = True


def read_db_one_festival(id_festival: int, session: Session) -> DBFestival:
    db_festival = session.query(DBFestival).filter(DBFestival.id_festival == id_festival).first()
    if db_festival is None:
        raise NotFoundError(f"Item with id {id_festival} not found.")
    return db_festival

def read_db_festival(session: Session) -> List[DBFestival]:
    db_festival = session.query(DBFestival).limit(5).all()
    if db_festival is None:
        raise NotFoundError(f"Database is empty")
    return db_festival

def generate_id(session: Session) -> int:
    """Generate a unique ID."""
    last_id = session.query(DBFestival.id_festival).order_by(DBFestival.id_festival.desc()).first()
    if last_id:
        last_id_number = last_id[0]
        new_id_number = last_id_number + 1
    else:
        new_id_number = 1000000000000001
    return new_id_number

def create_db_festival(festival: FestivalCreate, session: Session) -> DBFestival:
    db_festival = DBFestival(**festival.model_dump(exclude_none=True), id_festival=generate_id(session))
    session.add(db_festival)
    session.commit()
    session.refresh(db_festival)
    return db_festival

def update_db_festival(festival_id: int, festival: FestivalUpdate, session: Session) -> DBFestival:
    db_festival = read_db_one_festival(festival_id, session)
    for key, value in festival.model_dump(exclude_none=True).items():
        setattr(db_festival, key, value)
    session.commit()
    session.refresh(db_festival)
    return db_festival

def delete_db_festival(festival_id: int, session: Session) -> DBFestival:
    db_festival = read_db_one_festival(festival_id, session)
    session.delete(db_festival)
    session.commit()
    return db_festival
