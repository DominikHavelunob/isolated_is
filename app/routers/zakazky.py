from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import (
    get_current_user,
    user_exception,
    item_not_found_exception,
    je_admin,
    je_vedouci_mechanik,
    je_mechanik
)

router = APIRouter(prefix="/zakazky", tags=["Zakázky"])


@router.get("/{zakazka_id}", response_model=schemas.Zakazka)
def detail_zakazky(
    zakazka_id: UUID,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise item_not_found_exception
    if je_admin(current) or je_vedouci_mechanik(current):
        return zakazka
    if typ == "mechanik" and zakazka.mechanik_id == user.id:
        return zakazka
    if typ == "zakaznik" and zakazka.zakaznik_id == user.id:
        return zakazka
    raise user_exception




@router.get("/", response_model=list[schemas.Zakazka])
def seznam_zakazek(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current
    if je_admin(current) or je_vedouci_mechanik(current):
        return db.query(models.Zakazka).all()
    elif typ == "mechanik":
        return db.query(models.Zakazka).filter(models.Zakazka.mechanik_id == user.id).all()
    elif typ == "zakaznik":
        return db.query(models.Zakazka).filter(models.Zakazka.zakaznik_id == user.id).all()
    raise user_exception









# @router.post("/", response_model=schemas.Zakazka)
# def vytvorit_zakazku(
#     data: schemas.ZakazkaCreate,
#     current=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     user, typ = current
#     if not (typ == "mechanik" or je_vedouci_mechanik(current) or je_admin(current)):
#         raise user_exception

#     dict_data = data.model_dump()

#     if not dict_data.get("mechanik_id"):
#         dict_data["mechanik_id"] = user.id
#     dict_data["vytvoril_id"] = user.id

#     nova_zakazka = models.Zakazka(**dict_data)
#     db.add(nova_zakazka)
#     db.commit()
#     db.refresh(nova_zakazka)
#     return nova_zakazka

@router.post("/", response_model=schemas.Zakazka)
def vytvorit_zakazku(
    zakazka: schemas.ZakazkaCreate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current

    if not (typ == "mechanik" or je_vedouci_mechanik(current) or je_admin(current)):
        raise user_exception


    mechanik_id = zakazka.mechanik_id or user.id

 

    nova_zakazka = models.Zakazka(
        popis=zakazka.popis,
        stav=zakazka.stav or "otevřená",
        hotova = False,
        datum_prijmu=zakazka.datum_prijmu,
        datum_predani=zakazka.datum_predani,
        auto_znacka=zakazka.auto_znacka,
        auto_model=zakazka.auto_model,
        auto_vin=zakazka.auto_vin,
        cena=zakazka.cena,
        anonymizovana=False,
        smazano=False,
        zakaznik_id=zakazka.zakaznik_id,
        mechanik_id=mechanik_id,
#        vytvoril_id=user.id if je_mechanik(current) else None
    )

    db.add(nova_zakazka)
    db.commit()
    db.refresh(nova_zakazka)
    return nova_zakazka


# @router.post("/", response_model=schemas.Zakazka)
# def vytvorit_zakazku(
#     data: schemas.ZakazkaCreate,
#     current=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     user, typ = current
#     dict_data = data.model_dump()

#     # Logika přidělení mechanika
#     if typ in ["mechanik", "vedouci_mechanik"]:
#         dict_data["mechanik_id"] = user.id
#         dict_data["vytvoril_id"] = user.id
#     elif typ == "admin":
#         # Admin MUSÍ vybrat mechanika, nebo nechá prázdné (validace, pokud je potřeba)
#         if not dict_data.get("mechanik_id"):
#             dict_data["mechanik_id"] = None
#         dict_data["vytvoril_id"] = None
#     else:
#         raise user_exception

#     nova_zakazka = models.Zakazka(**dict_data)
#     db.add(nova_zakazka)
#     db.commit()
#     db.refresh(nova_zakazka)
#     return nova_zakazka


































@router.put("/{zakazka_id}", response_model=schemas.Zakazka)
def upravit_zakazku(
    zakazka_id: UUID,
    zakazka_update: schemas.ZakazkaUpdate,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user, typ = current
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise item_not_found_exception

    # --- ADMIN nebo VEDOUCI_MEKANIK mohou měnit vše ---
    if je_admin(current) or je_vedouci_mechanik(current):
        # Získáme jen ta pole, která uživatel opravdu poslal (ne None)
        for k, v in zakazka_update.dict(exclude_unset=True).items():
            setattr(zakazka, k, v)
        db.commit()
        db.refresh(zakazka)
        return zakazka

    # --- MECHANIK může měnit pouze svou zakázku (stav, popis) ---
    if je_mechanik(current) and zakazka.mechanik_id == user.id:
        for pole in ["stav", "popis"]:
            hodnota = getattr(zakazka_update, pole, None)
            if hodnota is not None:
                setattr(zakazka, pole, hodnota)
        db.commit()
        db.refresh(zakazka)
        return zakazka

    raise user_exception


@router.delete("/{zakazka_id}")
def smazat_zakazku(
    zakazka_id: UUID,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not je_admin(current) and not je_vedouci_mechanik(current):
        raise user_exception
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise item_not_found_exception
    db.delete(zakazka)
    db.commit()
    return {"detail": "Smazáno"}
