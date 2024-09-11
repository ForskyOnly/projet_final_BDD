from fastapi import FastAPI, APIRouter
from .database.db_core import get_db

app = FastAPI()

test_router = APIRouter()

# Importez les routers après avoir créé l'application
from festival_api.routers import festivals
from festival_api.routers import authentification

app.include_router(festivals.router)
app.include_router(authentification.router)

@app.get("/")
def read_root():
    """
    Cette fonction est la racine de l'application.
    Elle renvoie un message pour indiquer que le serveur est en cours d'exécution.
    """
    return "Server is running."

if __name__ == "__main__":
    """
    Cette bloc est le point d'entrée de l'application.
    Il démarre le serveur FastAPI avec uvicorn.
    """
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)