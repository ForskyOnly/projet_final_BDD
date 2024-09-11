from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from festival_api.main import app
from festival_api.database.db_core import Base, get_db
from festival_api.database.db_authentification import UserCreate, User, Token
import pytest

# Configuration de la base de données pour les tests c'est une base de données en mémoire qui afffecte pas le reste de l'application
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """
    Cette fonction est une surcharge de la fonction get_db pour les tests.
    Elle crée une nouvelle session de base de données pour les tests.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    Cette fonction est un fixture pour le client de test.
    Elle crée la base de données pour les tests et fournit un client de test pour les tests.
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_user(client):
    response = client.post(
        "/auth/create_user",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_for_access_token(client):
    # Créer un utilisateur d'abord
    """
    Cette fonction est un test pour vérifier si un utilisateur peut se connecter et obtenir un jeton d'accès.
    """
    client.post(
        "/auth/create_user",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_is_authorized(client):
    # Créer un utilisateur et obtenir un token valide
    """
    Cette fonction est un test pour vérifier si un utilisateur peut accéder à une ressource protégée.
    """
    client.post(
        "/auth/create_user",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    )
    login_response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/is_authorized",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == True

def test_unauthorized_access(client):
    """
    Cette fonction est un test pour vérifier si un utilisateur ne peut pas accéder à une ressource protégée avec un jeton invalide.
    """
    response = client.get(
        "/auth/is_authorized",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401