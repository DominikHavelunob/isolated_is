from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import SessionLocal, get_db
from app.utils import *

router = APIRouter(prefix="/zakaznici", tags=["Zákazníci"])


@router.get("/", response_model=list[schemas.Zakaznik])
def seznam_zakazniku(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    if je_admin(current) or je_vedouci_mechanik(current):
        return db.query(models.Zakaznik).all()
    raise user_exception

@router.get("/{zakaznik_id}", response_model=schemas.Zakaznik)
def detail_zakaznika(
    zakaznik_id: UUID,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise item_not_found_exception
    
    if je_admin(current) or je_vedouci_mechanik(current):
        return zakaznik

    if je_zakaznik(current):
        vyzaduje_vlastnika_uctu(zakaznik_id,current)
        return zakaznik        

    raise user_exception


@router.put("/{zakaznik_id}", response_model=schemas.Zakaznik)
def upravit_zakaznika(
    zakaznik_id: UUID, 
    data: schemas.ZakaznikCreate, 
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
    ):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise item_not_found_exception
    
    if je_admin(current):
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
    
    if je_zakaznik(current):
        vyzaduje_vlastnika_uctu(zakaznik_id, current)
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
    raise user_exception

@router.put("/anonymize/{zakaznik_id}")
def anonymizuj_zakaznika(
    zakaznik_id: UUID,
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
    ):
    zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
    if not zakaznik:
        raise item_not_found_exception  
    if je_admin(current) or je_zakaznik(current):
        if je_zakaznik(current):
            vyzaduje_vlastnika_uctu(zakaznik_id,current)
        zakaznik.jmeno = "Anonymizovano"
        zakaznik.prijmeni = "Anonymizovano"
        zakaznik.email = "anonymizovano_{zakaznik_id}@anonym.com"
        zakaznik.telefon = "Anonymizovano"
        zakaznik.adresa = "Anonymizovano"
        zakaznik.heslo = hash_heslo("Anonymizovano")
        db.commit()
        db.refresh(zakaznik)
        return zakaznik
    raise user_exception



@router.delete("/{zakaznik_id}")
def smazat_zakaznika(
    zakaznik_id: UUID,
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
    ):
    if je_admin(current):
        zakaznik = db.query(models.Zakaznik).filter(models.Zakaznik.id == zakaznik_id).first()
        if not zakaznik:
            raise item_not_found_exception
        db.delete(zakaznik)
        db.commit()
        return {"detail": "Smazáno"}
    raise user_exception
