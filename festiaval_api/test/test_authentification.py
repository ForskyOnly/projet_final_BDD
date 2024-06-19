from fastapi.testclient import TestClient
from main import app  
import pytest
from sqlalchemy.orm import Session
from database.core import get_db
from database.authentification import UserCreate, User, Token

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/auth/create_user",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data

def test_login_for_access_token():
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

def test_is_authorized():
    response = client.get(
        "/auth/is_authorized",
        headers={"Authorization": "Bearer token"},  
    )
    assert response.status_code == 200
    assert response.json() == True


