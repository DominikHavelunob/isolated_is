from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app import models, schemas, utils
from app.database import get_db
from app.utils import *

router = APIRouter(prefix="/auth", tags=["Autentizace"])

@router.post("/prihlaseni", response_model=schemas.Token)
def prihlaseni(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = None
    user_type = None


    admin = db.query(models.Admin).filter(models.Admin.email == form_data.username).first()
    if admin and over_heslo(form_data.password, admin.heslo):
        user = admin
        user_type = "admin"
    else:
        mech = db.query(models.Mechanik).filter(models.Mechanik.email == form_data.username).first()
        if mech and over_heslo(form_data.password, mech.heslo):
            user = mech
            user_type = "mechanik"
        else:
            zak = db.query(models.Zakaznik).filter(models.Zakaznik.email == form_data.username).first()
            if zak and not zak.smazano and not zak.anonymizovan and utils.over_heslo(form_data.password, zak.heslo):
                user = zak
                user_type = "zakaznik"

    if not user:
        raise general_exception

    access_token = utils.vytvor_access_token(
        #data={"sub": str(user.id), "typ_uzivatele": user_type},
        data={"sub": user.email, "typ_uzivatele": user_type},
        expires_delta=timedelta(minutes=60)
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Admin může registrovat mechaniky
# app/routers/auth.py


# registrace mechanika... generuje se email ve tvaru jmeno.prijmeni@firma.com, pripadne jmeno.prijmeni123@firma.com
@router.post("/registrace/mechanik", response_model=schemas.Mechanik)
def registrace_mechanika(
    mechanik: schemas.MechanikCreate, 
    db: Session = Depends(get_db),
    admin=Depends(vyzaduje_admina)
):
    base_email = f"{mechanik.jmeno.lower()}.{mechanik.prijmeni.lower()}@firma.com"
    email = base_email
    i = 2
    while db.query(models.Mechanik).filter(func.lower(models.Mechanik.email) == email).first():
        email = f"{mechanik.jmeno.lower()}.{mechanik.prijmeni.lower()}{i}@firma.com"
        i += 1

    if not minimalni_heslo(mechanik.heslo):
        raise HTTPException(status_code=400, detail="Slabé heslo. Musí mít aspoň 9 znaků a číslo.")

    nove_heslo = hash_heslo(mechanik.heslo)
    role_objekty = []
    if mechanik.role_ids:
        role_objekty = db.query(models.Role).filter(models.Role.id.in_(mechanik.role_ids)).all()
        if len(role_objekty) != len(mechanik.role_ids):
            raise HTTPException(status_code=400, detail="Jedna nebo více zvolených rolí neexistuje.")

    novy_mechanik = models.Mechanik(
        jmeno=mechanik.jmeno,
        prijmeni=mechanik.prijmeni,
        email=email,
        heslo=nove_heslo,
        telefon=mechanik.telefon,
        role=role_objekty
    )
    db.add(novy_mechanik)
    db.commit()
    db.refresh(novy_mechanik)
    return novy_mechanik


@router.post("/registrace/zakaznik", response_model=schemas.Zakaznik)
def registrace_zakaznika(zakaznik: schemas.ZakaznikCreate, db: Session = Depends(get_db)):
    shodny_email = db.query(models.Zakaznik).filter(
        models.Zakaznik.email == zakaznik.email,
        models.Zakaznik.smazano == False,
        models.Zakaznik.anonymizovan == False
    ).first()
    if shodny_email:
        raise HTTPException(status_code=400, detail="Email už existuje")
    
    shodny_email_mechanika = db.query(models.Mechanik).filter(
        models.Mechanik.email == zakaznik.email,
    ).first()
    if shodny_email_mechanika:
        raise HTTPException(status_code=400, detail="Email už existuje")

    if not minimalni_heslo(zakaznik.heslo):
        raise HTTPException(status_code=400, detail="Slabe heslo")
    nove_heslo = utils.hash_heslo(zakaznik.heslo)

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