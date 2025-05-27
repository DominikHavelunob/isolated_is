from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal, get_db
from app.utils import *

router = APIRouter(prefix="/mechanici", tags=["Mechanici"])


@router.get("/", response_model=list[schemas.Mechanik])
def seznam_mechaniku(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current
    if je_admin(current) or je_vedouci_mechanik(current):
        return db.query(models.Mechanik).all()
    elif typ == "mechanik":
        return [db.query(models.Mechanik).filter(models.Mechanik.id == user.id).first()]
    raise user_exception

@router.get("/{mechanik_id}", response_model=schemas.Mechanik)
def detail_mechanika(
    mechanik_id: UUID,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
    if not mechanik:
        raise item_not_found_exception
    if je_admin(current) or je_vedouci_mechanik(current):
        return mechanik
    if je_mechanik(current):
        vyzaduje_vlastnika_uctu(mechanik_id,current)
        return mechanik

    raise user_exception




# dodelat generovani emailu
@router.put("/{mechanik_id}", response_model=schemas.Mechanik)
def upravit_mechanika(
    mechanik_id: UUID,
    data: schemas.MechanikCreate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current
    mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
    if not mechanik:
        raise item_not_found_exception

    if je_admin(current):
        mechanik.jmeno = data.jmeno
        mechanik.prijmeni = data.prijmeni
        mechanik.email = data.email
        mechanik.telefon = data.telefon
        if data.heslo:
            mechanik.heslo = hash_heslo(data.heslo)
        if data.role_ids:
            mechanik.role = db.query(models.Role).filter(models.Role.id.in_(data.role_ids)).all()
        db.commit()
        db.refresh(mechanik)
        return mechanik

    if je_vedouci_mechanik(current) and user.id != mechanik_id:
        mechanik.telefon = data.telefon
        mechanik.email = data.email
        if data.role_ids:
            mechanik.role = db.query(models.Role).filter(models.Role.id.in_(data.role_ids)).all()
        db.commit()
        db.refresh(mechanik)
        return mechanik

    if typ == "mechanik" and user.id == mechanik_id:
        mechanik.jmeno = data.jmeno
        mechanik.prijmeni = data.prijmeni
        mechanik.email = data.email
        mechanik.telefon = data.telefon
        if data.heslo:
            mechanik.heslo = hash_heslo(data.heslo)
        db.commit()
        db.refresh(mechanik)
        return mechanik

    raise user_exception



@router.delete("/{mechanik_id}")
def smazat_mechanika(
    mechanik_id: UUID,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if je_admin(current):
        mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
        if not mechanik:
            raise item_not_found_exception
        db.delete(mechanik)
        db.commit()
        return {"detail": "Smazáno"}
    
    raise user_exception
