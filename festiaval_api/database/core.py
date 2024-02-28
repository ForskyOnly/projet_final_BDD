from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

class DBAdresse(Base):
    __tablename__ = 'adresse'
    id_adresse = Column(Integer, primary_key=True)
    adresse_postale = Column(String)
    code_insee = Column(String)
    region = Column(String)
    departement = Column(String)
    commune = Column(String)
    longitude = Column(Float)
    latitude = Column(Float())
    

# Classe pour les catégories
class DBCategorie(Base):
    __tablename__ = 'categorie'
    id_categorie = Column(Integer, primary_key=True)
    discipline_dominante = Column(String)
    sous_categorie = Column(String)

# Classe pour les périodes
class DBPeriode(Base):
    __tablename__ = 'periode'
    id_periode = Column(Integer, primary_key=True)
    periode = Column(String)
    categorie_periode = Column(String)

# Classe pour les festivals
class DBFestival(Base):
    __tablename__ = 'festival'
    id_festival = Column(Integer, primary_key=True)
    nom_festival = Column(String)
    annee_creation = Column(Integer)
    site_internet = Column(String)
    # Clés étrangères pour lier les adresses, catégories et périodes
    id_adresse = Column(Integer, ForeignKey('adresse.id_adresse', ondelete="CASCADE"))
    id_categorie = Column(Integer, ForeignKey('categorie.id_categorie', ondelete="CASCADE"))
    id_periode = Column(Integer, ForeignKey('periode.id_periode', ondelete="CASCADE"))

    # Configuration des relations
    adresse = relationship("DBAdresse", back_populates="festival", uselist=False)
    categorie = relationship("DBCategorie", back_populates="festival", uselist=False)
    periode = relationship("DBPeriode", back_populates="festival", uselist=False)

# Ajouter back_populates dans les autres classes
DBAdresse.festival = relationship("DBFestival", back_populates="adresse")
DBCategorie.festival = relationship("DBFestival", back_populates="categorie")
DBPeriode.festival = relationship("DBFestival", back_populates="periode")


class DBUsers(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    tokens = relationship("DBToken", back_populates="user")  

class DBToken(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("DBUsers", back_populates="tokens")
    
class NotFoundError(Exception):
    pass


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
