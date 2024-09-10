import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

# Charger les variables d'environnement
load_dotenv()

# Déterminer l'URL de la base de données
if os.environ.get('TESTING') == 'True':
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL and not DATABASE_URL.startswith('sqlite:///'):
        DATABASE_URL = f"sqlite:///{DATABASE_URL}"

# Créer le moteur de base de données
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Créer une base déclarative
Base = declarative_base()

# Définition des modèles
class DBAdresse(Base):
    __tablename__ = 'adresse'
    id_adresse = Column(Integer, primary_key=True)
    adresse_postale = Column(String)
    code_insee = Column(String)
    region = Column(String)
    departement = Column(String)
    commune = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    festival = relationship("DBFestival", back_populates="adresse", uselist=False)

class DBCategorie(Base):
    __tablename__ = 'categorie'
    id_categorie = Column(Integer, primary_key=True)
    discipline_dominante = Column(String)
    sous_categorie = Column(String)
    festival = relationship("DBFestival", back_populates="categorie", uselist=False)

class DBPeriode(Base):
    __tablename__ = 'periode'
    id_periode = Column(Integer, primary_key=True)
    periode = Column(String)
    categorie_periode = Column(String)
    festival = relationship("DBFestival", back_populates="periode", uselist=False)

class DBFestival(Base):
    __tablename__ = 'festival'
    id_festival = Column(Integer, primary_key=True)
    nom_festival = Column(String)
    annee_creation = Column(Integer)
    site_internet = Column(String)
    id_adresse = Column(Integer, ForeignKey('adresse.id_adresse', ondelete="CASCADE"))
    id_categorie = Column(Integer, ForeignKey('categorie.id_categorie', ondelete="CASCADE"))
    id_periode = Column(Integer, ForeignKey('periode.id_periode', ondelete="CASCADE"))
    adresse = relationship("DBAdresse", back_populates="festival")
    categorie = relationship("DBCategorie", back_populates="festival")
    periode = relationship("DBPeriode", back_populates="festival")


class DBUsers(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, nullable=True)
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

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
