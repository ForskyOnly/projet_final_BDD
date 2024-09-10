import pytest
from httpx import AsyncClient
from festival_api.main import app
import random
import string
from festival_api.database.db_core import Base, engine, get_db
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def auth_header(client):
    user_data = {
        "username": f"testuser_{random_string()}",
        "password": "testpassword",
        "email": f"testuser_{random_string()}@example.com",
        "full_name": "Test User"
    }
    response = client.post("/auth/create_user", json=user_data)
    assert response.status_code == 200
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_festival(auth_header, client):
    festival_data = {
        "nom_festival": f"Festival de Test {random_string()}",
        "annee_creation": 2023,
        "site_internet": "http://test.com",
        "adresse": {
            "adresse_postale": "1 Rue de Test",
            "code_insee": "75001",
            "region": "Île-de-France",
            "departement": "Paris",
            "commune": "Paris",
            "longitude": 2.3522,
            "latitude": 48.8566
        },
        "categorie": {
            "discipline_dominante": "Musique",
            "sous_categorie": "Rock"
        },
        "periode": {
            "periode": "Été",
            "categorie_periode": "Saisonnier"
        }
    }
    response = client.post("/festivals/", json=festival_data, headers=auth_header)
    assert response.status_code == 200, f"Statut de réponse inattendu: {response.status_code}"
    created_festival = response.json()
    print("Réponse complète:", created_festival)  # Ajoutez cette ligne
    assert "id_festival" in created_festival, f"La clé 'id_festival' est manquante dans la réponse. Réponse reçue : {created_festival}"

@pytest.mark.asyncio
async def test_get_festival(auth_header, client):
    festival_id = await test_create_festival(auth_header, client)
    response = client.get(f"/festivals/{festival_id}", headers=auth_header)
    assert response.status_code == 200, f"Statut de réponse inattendu: {response.status_code}"
    festival = response.json()
    assert "nom_festival" in festival, "La clé 'nom_festival' est manquante dans la réponse"
    assert festival["nom_festival"].startswith("Festival de Test")

@pytest.mark.asyncio
async def test_update_festival(auth_header, client):
    festival_id = await test_create_festival(auth_header, client)
    update_data = {
        "nom_festival": "Festival de Test Mis à Jour",
        "annee_creation": 2024,
        "site_internet": "http://test-updated.com",
        "adresse": {
            "adresse_postale": "2 Rue de Test",
            "code_insee": "75002",
            "region": "Île-de-France",
            "departement": "Paris",
            "commune": "Paris",
            "longitude": 2.3522,
            "latitude": 48.8566
        },
        "categorie": {
            "discipline_dominante": "Musique",
            "sous_categorie": "Jazz"
        },
        "periode": {
            "periode": "Hiver",
            "categorie_periode": "Saisonnier"
        }
    }
    response = client.put(f"/festivals/{festival_id}", json=update_data, headers=auth_header)
    assert response.status_code == 200, f"Statut de réponse inattendu: {response.status_code}"
    updated_festival = response.json()
    assert updated_festival["nom_festival"] == "Festival de Test Mis à Jour"
    assert updated_festival["annee_creation"] == 2024

@pytest.mark.asyncio
async def test_delete_festival(auth_header, client):
    festival_id = await test_create_festival(auth_header, client)
    response = client.delete(f"/festivals/{festival_id}", headers=auth_header)
    assert response.status_code == 204, f"Statut de réponse inattendu: {response.status_code}"

@pytest.mark.asyncio
async def test_get_all_festivals(auth_header, client):
    await test_create_festival(auth_header, client)
    await test_create_festival(auth_header, client)
    response = client.get("/festivals/", headers=auth_header)
    assert response.status_code == 200, f"Statut de réponse inattendu: {response.status_code}"
    festivals = response.json()
    assert isinstance(festivals, list), "La réponse devrait être une liste"
    assert len(festivals) >= 2, "Il devrait y avoir au moins 2 festivals"

@pytest.mark.asyncio
async def test_get_nonexistent_festival(auth_header, client):
    nonexistent_id = 9999
    response = client.get(f"/festivals/{nonexistent_id}", headers=auth_header)
    assert response.status_code == 404, f"Statut de réponse inattendu: {response.status_code}"