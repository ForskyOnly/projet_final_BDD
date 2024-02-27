from fastapi import FastAPI, APIRouter
from routers import festivals, authentification

test_router = APIRouter()

app = FastAPI()

app.include_router(festivals.router, prefix="/festivals")
app.include_router(authentification.router, prefix="/authentification")

@app.get("/")
def read_root():
    return "Server is running."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
