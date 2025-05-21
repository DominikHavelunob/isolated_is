from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal

router = APIRouter(prefix="/zakaznici", tags=["Zákazníci"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.Zakaznik])
def seznam_zakazniku(db: Session = Depends(get_db)):
    return db.query(models.Zakaznik).all()

@router.get("/{zakaznik_id}", response_model=schemas.Zakaznik)
def detail_zakaznika(zakaznik_id: int, db: Session = Depends(get_db)):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise HTTPException(status_code=404, detail="Zákazník nenalezen")
    return zakaznik

@router.put("/{zakaznik_id}", response_model=schemas.Zakaznik)
def upravit_zakaznika(zakaznik_id: int, data: schemas.ZakaznikCreate, db: Session = Depends(get_db)):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise HTTPException(status_code=404, detail="Zákazník nenalezen")
    zakaznik.jmeno = data.jmeno
    zakaznik.prijmeni = data.prijmeni
    zakaznik.email = data.email
    zakaznik.telefon = data.telefon
    zakaznik.adresa = data.adresa
    if data.heslo:
        zakaznik.heslo = utils.hash_heslo(data.heslo)
    db.commit()
    db.refresh(zakaznik)
    return zakaznik

@router.delete("/{zakaznik_id}")
def smazat_zakaznika(zakaznik_id: int, db: Session = Depends(get_db)):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise HTTPException(status_code=404, detail="Zákazník nenalezen")
    db.delete(zakaznik)
    db.commit()
    return {"detail": "Smazáno"}
