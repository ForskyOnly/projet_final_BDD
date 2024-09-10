from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modèles SQLAlchemy pour la base de données

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

class Adresse(Base):
    __tablename__ = "adresses"

    id = Column(Integer, primary_key=True, index=True)
    adresse_postale = Column(String)
    code_insee = Column(String)
    region = Column(String)
    departement = Column(String)
    commune = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    festivals = relationship("Festival", back_populates="adresse")

class Categorie(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    discipline_dominante = Column(String)
    sous_categorie = Column(String)

    festivals = relationship("Festival", back_populates="categorie")

class Periode(Base):
    __tablename__ = "periodes"

    id = Column(Integer, primary_key=True, index=True)
    periode = Column(String)
    categorie_periode = Column(String)

    festivals = relationship("Festival", back_populates="periode")

class Festival(Base):
    __tablename__ = "festivals"

    id = Column(Integer, primary_key=True, index=True)
    nom_festival = Column(String, index=True)
    annee_creation = Column(Integer)
    site_internet = Column(String, nullable=True)
    id_adresse = Column(Integer, ForeignKey("adresses.id"))
    id_categorie = Column(Integer, ForeignKey("categories.id"))
    id_periode = Column(Integer, ForeignKey("periodes.id"))

    adresse = relationship("Adresse", back_populates="festivals")
    categorie = relationship("Categorie", back_populates="festivals")
    periode = relationship("Periode", back_populates="festivals")

# Modèles Pydantic pour la validation et la sérialisation

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True

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
    nom_festival: str
    annee_creation: int
    site_internet: Optional[str] = None
    id_adresse: int
    id_categorie: int
    id_periode: int

class FestivalCreate(FestivalBase):
    pass

class FestivalResponse(FestivalBase):
    id: int

    class Config:
        from_attributes = True