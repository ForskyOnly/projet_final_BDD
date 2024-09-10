import os
import pytest
from sqlalchemy.orm import Session

os.environ['TESTING'] = 'True'

from festival_api.database.db_authentification import create_db_user, get_user, UserCreate
from festival_api.database.db_core import NotFoundError, DBUsers, DBFestival, DBAdresse, DBCategorie, DBPeriode, SessionLocal, Base
from festival_api.database.db_festivals import create_db_festival, update_db_festival, delete_db_festival, read_db_one_festival, FestivalCreate, FestivalUpdate, AdresseBase, CategorieBase, PeriodeBase

@pytest.fixture(scope="function")
def db():
    db = SessionLocal()
    Base.metadata.create_all(bind=db.bind)
    try:
        yield db
    finally:
        db.rollback()
        Base.metadata.drop_all(bind=db.bind)
        db.close()

def test_create_user(db: Session):
    user_data = UserCreate(username="testuser", email="test@example.com", password="testpassword")
    new_user = create_db_user(user_data, db)
    
    assert new_user.username == "testuser"
    assert new_user.email == "test@example.com"
    assert new_user.hashed_password != "testpassword"

def test_get_user(db: Session):
    user_data = UserCreate(username="testuser2", email="test2@example.com", password="testpassword2")
    create_db_user(user_data, db)
    
    retrieved_user = get_user("testuser2", db)
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser2"
    assert retrieved_user.email == "test2@example.com"

def test_create_festival(db: Session):
    festival_data = FestivalCreate(
        nom_festival="Festival de Test",
        annee_creation=2023,
        site_internet="http://test.com",
        adresse=AdresseBase(
            adresse_postale="1 Rue de Test",
            code_insee="75001",
            region="Île-de-France",
            departement="Paris",
            commune="Paris",
            longitude=2.3522,
            latitude=48.8566
        ),
        categorie=CategorieBase(
            discipline_dominante="Musique",
            sous_categorie="Rock"
        ),
        periode=PeriodeBase(
            periode="Été",
            categorie_periode="Saisonnier"
        )
    )
    new_festival = create_db_festival(festival_data, db)
    
    assert new_festival.nom_festival == "Festival de Test"
    assert new_festival.annee_creation == 2023
    assert new_festival.site_internet == "http://test.com"
    assert new_festival.adresse.commune == "Paris"
    assert new_festival.categorie.discipline_dominante == "Musique"
    assert new_festival.periode.periode == "Été"

def test_get_festival(db: Session):
    festival_data = FestivalCreate(
        nom_festival="Festival de Récupération",
        annee_creation=2024,
        site_internet="http://recuperation.com",
        adresse=AdresseBase(
            adresse_postale="2 Rue de Récupération",
            code_insee="75002",
            region="Île-de-France",
            departement="Paris",
            commune="Paris",
            longitude=2.3522,
            latitude=48.8566
        ),
        categorie=CategorieBase(
            discipline_dominante="Théâtre",
            sous_categorie="Contemporain"
        ),
        periode=PeriodeBase(
            periode="Printemps",
            categorie_periode="Saisonnier"
        )
    )
    created_festival = create_db_festival(festival_data, db)
    
    retrieved_festival = read_db_one_festival(created_festival.id_festival, db)
    assert retrieved_festival is not None
    assert retrieved_festival.nom_festival == "Festival de Récupération"
    assert retrieved_festival.annee_creation == 2024

def test_update_festival(db: Session):
    festival_data = FestivalCreate(
        nom_festival="Festival à Mettre à Jour",
        annee_creation=2025,
        site_internet="http://update.com",
        adresse=AdresseBase(
            adresse_postale="3 Rue de Mise à Jour",
            code_insee="75003",
            region="Île-de-France",
            departement="Paris",
            commune="Paris",
            longitude=2.3522,
            latitude=48.8566
        ),
        categorie=CategorieBase(
            discipline_dominante="Danse",
            sous_categorie="Contemporaine"
        ),
        periode=PeriodeBase(
            periode="Automne",
            categorie_periode="Saisonnier"
        )
    )
    created_festival = create_db_festival(festival_data, db)
    
    updated_data = FestivalUpdate(
        nom_festival="Festival Mis à Jour",
        annee_creation=2026,
        site_internet="http://updated.com",
        adresse=AdresseBase(
            adresse_postale="3 Rue Mise à Jour",
            code_insee="75003",
            region="Île-de-France",
            departement="Paris",
            commune="Paris",
            longitude=2.3522,
            latitude=48.8566
        ),
        categorie=CategorieBase(
            discipline_dominante="Danse",
            sous_categorie="Moderne"
        ),
        periode=PeriodeBase(
            periode="Hiver",
            categorie_periode="Saisonnier"
        )
    )
    updated_festival = update_db_festival(created_festival.id_festival, updated_data, db)
    
    assert updated_festival.nom_festival == "Festival Mis à Jour"
    assert updated_festival.annee_creation == 2026
    assert updated_festival.site_internet == "http://updated.com"
    assert updated_festival.categorie.sous_categorie == "Moderne"
    assert updated_festival.periode.periode == "Hiver"



def test_delete_festival(db: Session):
    festival_data = FestivalCreate(
        nom_festival="Festival à Supprimer",
        annee_creation=2027,
        site_internet="http://delete.com",
        adresse=AdresseBase(
            adresse_postale="4 Rue de Suppression",
            code_insee="75004",
            region="Île-de-France",
            departement="Paris",
            commune="Paris",
            longitude=2.3522,
            latitude=48.8566
        ),
        categorie=CategorieBase(
            discipline_dominante="Cinéma",
            sous_categorie="Court-métrage"
        ),
        periode=PeriodeBase(
            periode="Hiver",
            categorie_periode="Saisonnier"
        )
    )
    created_festival = create_db_festival(festival_data, db)
    
    # Vérifiez que le festival existe avant la suppression
    assert read_db_one_festival(created_festival.id_festival, db) is not None
    
    # Supprimez le festival
    delete_db_festival(created_festival.id_festival, db)
    
    # Vérifiez que le festival n'existe plus
    with pytest.raises(NotFoundError):
        read_db_one_festival(created_festival.id_festival, db)