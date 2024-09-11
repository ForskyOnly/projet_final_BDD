from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .db_core import DBUsers, DBToken, NotFoundError, get_db
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()


class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    password: str

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def create_db_user(user: UserCreate, db: Session) -> DBUsers:
    """
    Cette fonction crée un nouvel utilisateur dans la base de données.
    C'est comme enregistrer un nouveau participant dans le grand livre du festival !
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = DBUsers(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    """
    Cette fonction vérifie si le mot de passe en clair correspond au mot de passe haché.
    C'est comme vérifier si la clé d'un coffre-fort correspond à la bonne combinaison !
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    Cette fonction crée un hachage du mot de passe en clair.
    C'est comme transformer une phrase en code secret pour protéger ton coffre-fort !
    """
    return pwd_context.hash(password)

def get_user(username: str, db: Session) -> Optional[DBUsers]:
    """
    Cette fonction récupère un utilisateur à partir du nom d'utilisateur.
    C'est comme trouver une personne dans un annuaire par son nom !
    """
    return db.query(DBUsers).filter(DBUsers.username == username).first()

def authenticate_user(db: Session, username: str, password: str) -> Optional[DBUsers]:
    user = get_user(username, db)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cette fonction crée un jeton d'accès.
    C'est comme créer un badge VIP pour votre API !
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> DBUsers:
    """
    Cette fonction récupère l'utilisateur actuel à partir du jeton d'accès.
    C'est comme retrouver la personne derrière le badge VIP !
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username, db)
    if user is None:
        raise credentials_exception
    return user

async def has_access(current_user: DBUsers = Depends(get_current_user)) -> DBUsers:
    """
    Cette fonction vérifie si l'utilisateur a le droit d'accéder à une ressource protégée.
    C'est comme un videur à l'entrée d'une boîte de nuit VIP :
    il vérifie votre badge (le token) et s'assure que vous êtes sur la liste des invités 
    (dans la base de données) avant de vous laisser entrer !
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

def user_to_pydantic(db_user: DBUsers) -> User:
    """
    Cette fonction convertit un utilisateur de la base de données en un utilisateur Pydantic.
    C'est comme transformer une photo en miniature pour l'afficher dans un album !
    """
    return User(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        disabled=db_user.disabled
    )