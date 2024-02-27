from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

Base = declarative_base()

class DBFestival(Base):
    __tablename__ = "festival"

    id_festival = Column(Integer, primary_key=True, index=True)
    nom_festival = Column(String)
    region = Column(String)
    departement = Column(String)
    commune = Column(String)
    code_insee = Column(String)
    site_internet = Column(String)
    annee_creation = Column(Integer)
    discipline_principale = Column(String)
    sous_categorie = Column(String)
    periode = Column(String)
    longitude = Column(String)
    latitude = Column(String)
    categorie_periode = Column(String)
    adresse_postale = Column(String)


class DBUsers(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    tokens = relationship("Token", back_populates="user")


class NotFoundError(Exception):
    pass

class DBToken(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    token_type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
