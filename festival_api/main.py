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
    return "Server is running."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)