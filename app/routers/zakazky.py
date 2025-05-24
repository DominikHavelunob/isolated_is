from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, get_db
from app.utils import get_current_user


router = APIRouter(prefix="/zakazky", tags=["Zakázky"])
user_exception = HTTPException(status_code=403, detail="Nepovoleny uzivatel")
item_not_found_exception = HTTPException(status_code=404, detail="Polozka nenalezena")

@router.get("/", response_model=list[schemas.Zakazka])
def seznam_zakazek(db: Session = Depends(get_db)):
    return db.query(models.Zakazka).all()

@router.get("/{zakazka_id}", response_model=schemas.Zakazka)
def detail_zakazky(zakazka_id: int, db: Session = Depends(get_db)):
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise HTTPException(status_code=404, detail="Zakázka nenalezena")
    return zakazka

# o2auth zkouska
@router.post("/", response_model=schemas.Zakazka)
def vytvorit_zakazku(
    data: schemas.ZakazkaCreate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user)
):
    user, typ = current
    if typ != "mechanik":
        raise user_exception

#    dict_data = data.dict()
    dict_data = data.model_dump()
    if not dict_data.get("mechanik_id"):
        dict_data["mechanik_id"] = user.id

    nova_zakazka = models.Zakazka(**dict_data)
    db.add(nova_zakazka)
    db.commit()
    db.refresh(nova_zakazka)
    return nova_zakazka
# ====

@router.put("/{zakazka_id}", response_model=schemas.Zakazka)
def upravit_zakazku(
    zakazka_id: int,
    data: schemas.ZakazkaBase,
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):
    user, typ = current
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise item_not_found_exception

    if typ != "mechanik" or zakazka.mechanik_id != user.id:
        raise user_exception


    dict_data = data.model_dump()
    if not dict_data.get("mechanik_id"):
        dict_data["mechanik_id"] = zakazka.mechanik_id  # nebo user.id, ale stejne nikdo
                                                        # jiny nez opravneny mechanik 
                                                        # nemuze menit zakazku 
                                                        # (ochrana pred admin id)

    for key, value in dict_data.items():
        setattr(zakazka, key, value)

    db.commit()
    db.refresh(zakazka)
    return zakazka


#adf


# @router.put("/{zakazka_id}", response_model=schemas.Zakazka)
# def upravit_zakazku(zakazka_id: int, data: schemas.ZakazkaCreate, db: Session = Depends(get_db)):
#     zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
#     if not zakazka:
#         raise HTTPException(status_code=404, detail="Zakázka nenalezena")
#     for key, value in data.dict().items():
#         setattr(zakazka, key, value)
#     db.commit()
#     db.refresh(zakazka)
#     return zakazka


@router.delete("/{zakazka_id}", response_model=schemas.Zakazka)
def smazat_zakazku(
    zakazka_id: int,
    db: Session = Depends(get_db),
    current = Depends(get_current_user)
):
    user, typ = current


    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise item_not_found_exception


    if typ != "mechanik" or zakazka.mechanik_id != user.id:
        raise user_exception



    db.delete(zakazka)
    db.commit()
    return {"detail": "Smazáno"}


# @router.delete("/{zakazka_id}")
# def smazat_zakazku(zakazka_id: int, db: Session = Depends(get_db)):
#     zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
#     if not zakazka:
#         raise HTTPException(status_code=404, detail="Zakázka nenalezena")
#     db.delete(zakazka)
#     db.commit()
#     return {"detail": "Smazáno"}