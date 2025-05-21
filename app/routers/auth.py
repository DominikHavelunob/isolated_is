from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.utils import minimalni_heslo
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Autentizace"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/prihlaseni", response_model=schemas.Token)
def prihlaseni(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # První pokus o přihlášení jako mechanik
    uzivatel = db.query(models.Mechanik).filter(models.Mechanik.email == form_data.username).first()
    typ_uzivatele = "mechanik"
    if not uzivatel:
        # Pokud neexistuje, zkusíme jako zákazník
        uzivatel = db.query(models.Zakaznik).filter(models.Zakaznik.email == form_data.username).first()
        typ_uzivatele = "zakaznik"
    if not uzivatel or not utils.over_heslo(form_data.password, uzivatel.heslo):
        raise HTTPException(status_code=400, detail="Nesprávný email nebo heslo")
    # JWT token - typ uživatele je součástí claimu
    access_token = utils.vytvor_access_token(
        data={"sub": uzivatel.email, "typ_uzivatele": typ_uzivatele},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Admin může registrovat mechaniky
# app/routers/auth.py

from sqlalchemy import func

# registrace mechanika... generuje se email ve tvaru jmeno.prijmeni@firma.com, pripadne jmeno.prijmeni123@firma.com
@router.post("/registrace/mechanik", response_model=schemas.Mechanik)
def registrace_mechanika(mechanik: schemas.MechanikCreate, db: Session = Depends(get_db)):
    base_email = f"{mechanik.jmeno.lower()}.{mechanik.prijmeni.lower()}@firma.com"
    email = base_email
    i = 2

    while db.query(models.Mechanik).filter(func.lower(models.Mechanik.email) == email).first():
        email = f"{mechanik.jmeno.lower()}.{mechanik.prijmeni.lower()}{i}@firma.com"
        i += 1

    # basic validace hesla
    if(minimalni_heslo(mechanik.heslo)):
        nove_heslo = utils.hash_heslo(mechanik.heslo)
    else:
        raise HTTPException(status_code=400, detail="Slabe heslo")

    #nove_heslo = utils.hash_heslo(mechanik.heslo)
    novy_mechanik = models.Mechanik(
        jmeno=mechanik.jmeno,
        prijmeni=mechanik.prijmeni,
        email=email,
        heslo=nove_heslo,
        telefon=mechanik.telefon
    )
    if mechanik.role_ids:
        novy_mechanik.role = db.query(models.Role).filter(models.Role.id.in_(mechanik.role_ids)).all()
    db.add(novy_mechanik)
    db.commit()
    db.refresh(novy_mechanik)
    return novy_mechanik

@router.post("/registrace/zakaznik", response_model=schemas.Zakaznik)
def registrace_zakaznika(zakaznik: schemas.ZakaznikCreate, db: Session = Depends(get_db)):
    if db.query(models.Zakaznik).filter(models.Zakaznik.email == zakaznik.email).first():
        raise HTTPException(status_code=400, detail="Email už existuje")
    

    if(minimalni_heslo(zakaznik.heslo)):
        nove_heslo = utils.hash_heslo(zakaznik.heslo)
    else:
        raise HTTPException(status_code=400, detail="Slabe heslo")
    novy_zakaznik = models.Zakaznik(
        jmeno=zakaznik.jmeno,
        prijmeni=zakaznik.prijmeni,
        email=zakaznik.email,
        heslo=nove_heslo,
        telefon=zakaznik.telefon,
        adresa=zakaznik.adresa
    )
    db.add(novy_zakaznik)
    db.commit()
    db.refresh(novy_zakaznik)
    return novy_zakaznik
