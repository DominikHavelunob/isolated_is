from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app import  schemas
from app.database import SessionLocal, get_db
from app.utils import *

router = APIRouter(prefix="/admini", tags=["Admin"])

@router.get("/")
def test_admin(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if je_admin(current):
        return {"detail": "gratuluji, jsi admin"}
    else:
        return {"detail": "get the fuck out"}