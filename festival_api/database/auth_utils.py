from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .db_core import DBUsers, DBToken, NotFoundError, get_db
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .db_authentification import get_user

from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def has_access(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    """
    Cette fonction vérifie si l'utilisateur a le droit d'accéder à une ressource protégée.
    
    Elle fonctionne comme suit :
    1. Elle essaie de décoder le token JWT fourni.
    2. Si le décodage réussit, elle extrait le nom d'utilisateur du token.
    3. Elle vérifie ensuite si cet utilisateur existe dans la base de données.
    4. Si tout est en ordre, elle renvoie les informations de l'utilisateur.
    
    Si quelque chose ne va pas (token invalide, utilisateur inexistant, etc.),
    elle lance une exception indiquant que l'authentification a échoué.
    
    C'est comme un videur à l'entrée d'une boîte de nuit VIP :
    il vérifie votre badge (le token) et s'assure que vous êtes sur la liste des invités 
    (dans la base de données) avant de vous laisser entrer !
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
        db_user = get_user(username, session) 
        if db_user is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    return db_user