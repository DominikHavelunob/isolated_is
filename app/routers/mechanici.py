from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal

router = APIRouter(prefix="/mechanici", tags=["Mechanici"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Mechanik])
def seznam_mechaniku(db: Session = Depends(get_db)):
    return db.query(models.Mechanik).all()

@router.get("/{mechanik_id}", response_model=schemas.Mechanik)
def detail_mechanika(mechanik_id: int, db: Session = Depends(get_db)):
    mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
    if not mechanik:
        raise HTTPException(status_code=404, detail="Mechanik nenalezen")
    return mechanik

@router.put("/{mechanik_id}", response_model=schemas.Mechanik)
def upravit_mechanika(mechanik_id: int, data: schemas.MechanikCreate, db: Session = Depends(get_db)):
    mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
    if not mechanik:
        raise HTTPException(status_code=404, detail="Mechanik nenalezen")
    mechanik.jmeno = data.jmeno
    mechanik.prijmeni = data.prijmeni
    mechanik.email = data.email
    mechanik.telefon = data.telefon
    if data.heslo:
        mechanik.heslo = utils.hash_heslo(data.heslo)
    if data.role_ids:
        mechanik.role = db.query(models.Role).filter(models.Role.id.in_(data.role_ids)).all()
    db.commit()
    db.refresh(mechanik)
    return mechanik

@router.delete("/{mechanik_id}")
def smazat_mechanika(mechanik_id: int, db: Session = Depends(get_db)):
    mechanik = db.query(models.Mechanik).filter(models.Mechanik.id == mechanik_id).first()
    if not mechanik:
        raise HTTPException(status_code=404, detail="Mechanik nenalezen")
    db.delete(mechanik)
    db.commit()
    return {"detail": "Smazáno"}
