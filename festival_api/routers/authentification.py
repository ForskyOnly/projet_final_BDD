from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..database.db_core import get_db, DBUsers
from ..database.db_authentification import Token, User, UserCreate, authenticate_user, create_db_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash
from festival_api.database.auth_utils import has_access
from festival_api.main import app  




router = APIRouter(
    prefix="/auth",
)

@router.post("/create_user", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Cette fonction crée un nouvel utilisateur dans la base de données.
    C'est comme enregistrer un nouveau participant dans le grand livre du festival !
    """
    db_user = create_db_user(user, db)
    return db_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def create_db_user(user: UserCreate, session: Session):
    """
    Cette fonction crée un nouvel utilisateur dans la base de données.
    C'est comme enregistrer un nouveau participant dans le grand livre du festival !
    """
    hashed_password = get_password_hash(user.password)
    db_user = DBUsers(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        request: Request,
        db: Session = Depends(get_db)) -> Token:    
    """
    Cette fonction permet à un utilisateur de se connecter et de recevoir un jeton d'accès.
    C'est comme obtenir une clé pour ouvrir une porte de vérification !
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")



@router.get("/is_authorized", response_model=None)
async def is_authorized(current_user: Annotated[User, Depends(has_access)]):
    """
    Cette fonction vérifie si l'utilisateur est autorisé à accéder à une ressource.
    C'est comme vérifier si vous avez le droit d'entrer dans une pièce spécifique !
    """
    return True