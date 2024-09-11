from fastapi import APIRouter, HTTPException, Request, status, Depends, Response
from ..database import db_authentification
from sqlalchemy.orm import Session
from typing import List
from ..database.db_core import NotFoundError, get_db
from ..database.db_authentification import User
from ..database.db_festivals import Festival, FestivalCreate, FestivalUpdate, read_db_festival, read_db_one_festival, \
    create_db_festival, update_db_festival, delete_db_festival
from fastapi import APIRouter, Depends, HTTPException, status
from ..database.db_core import DBFestival
from ..database.db_authentification import has_access

router = APIRouter(
    prefix="/festivals",
)

PROTECTED = Depends(db_authentification.has_access)



@router.get("/{festival_id}", response_model=Festival)
def get_one_festival(festival_id: int, request: Request, db: Session = Depends(get_db)) -> Festival:
    """
    Cette fonction récupère un festival spécifique de la base de données.
    C'est comme trouver un événement spécifique dans le calendrier du festival !
    """
    try:
        db_festival = read_db_one_festival(festival_id, db)
    except NotFoundError as e:  
        raise HTTPException(status_code=404, detail=str(e))
    return db_festival


@router.get("/", response_model=List[Festival])
def get_festivals(request: Request, db: Session = Depends(get_db)) -> List[Festival]:
    """
    Cette fonction récupère tous les festivals de la base de données.
    C'est comme regarder tous les événements dans le calendrier du festival !
    """
    try:
        db_festivals = read_db_festival(db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return db_festivals


@router.post("/", response_model=Festival)
def create_festival(festival: FestivalCreate, db: Session = Depends(get_db), has_access: User = PROTECTED) -> Festival:
    """
    Cette fonction crée un nouveau festival dans la base de données.
    C'est comme ajouter un nouvel événement dans le calendrier du festival !
    """
    db_festival = create_db_festival(festival, db)
    return db_festival


@router.put("/{festival_id}", response_model=Festival)
def update_festival(festival_id: int, festival: FestivalUpdate, db: Session = Depends(get_db), has_access: User = PROTECTED) -> Festival:
    """
    Cette fonction met à jour un festival existant dans la base de données.
    C'est comme modifier les informations d'un événement dans le calendrier du festival !
    """
    try:
        db_festival = update_db_festival(festival_id, festival, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return db_festival

@router.delete("/{festival_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_festival_endpoint(festival_id: int, db: Session = Depends(get_db)):
    """
    Cette fonction supprime un festival spécifique de la base de données.
    C'est comme enlever un événement du calendrier du festival !
    """
    success = delete_db_festival(festival_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Festival not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
