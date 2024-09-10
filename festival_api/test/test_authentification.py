from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from festival_api.main import app
from festival_api.database.db_core import Base, get_db
from festival_api.database.db_authentification import UserCreate, User, Token
import pytest

# Configuration de la base de données pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
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
    response = client.get(
        "/auth/is_authorized",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401