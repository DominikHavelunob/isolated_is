from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, get_db
from app.utils import get_current_user


router = APIRouter(prefix="/zakazky", tags=["Zakázky"])


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
        raise HTTPException(status_code=403, detail="Pouze mechanik muze zalozit zakazku")

    dict_data = data.dict()
    if not dict_data.get("mechanik_id"):
        dict_data["mechanik_id"] = user.id

    nova_zakazka = models.Zakazka(**dict_data)
    db.add(nova_zakazka)
    db.commit()
    db.refresh(nova_zakazka)
    return nova_zakazka
# ====

# @router.post("/", response_model=schemas.Zakazka)
# def vytvorit_zakazku(data: schemas.ZakazkaCreate, db: Session = Depends(get_db)):
#     nova_zakazka = models.Zakazka(**data.dict())
#     db.add(nova_zakazka)
#     db.commit()
#     db.refresh(nova_zakazka)
#     return nova_zakazka

@router.put("/{zakazka_id}", response_model=schemas.Zakazka)
def upravit_zakazku(zakazka_id: int, data: schemas.ZakazkaCreate, db: Session = Depends(get_db)):
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise HTTPException(status_code=404, detail="Zakázka nenalezena")
    for key, value in data.dict().items():
        setattr(zakazka, key, value)
    db.commit()
    db.refresh(zakazka)
    return zakazka

@router.delete("/{zakazka_id}")
def smazat_zakazku(zakazka_id: int, db: Session = Depends(get_db)):
    zakazka = db.query(models.Zakazka).filter(models.Zakazka.id == zakazka_id).first()
    if not zakazka:
        raise HTTPException(status_code=404, detail="Zakázka nenalezena")
    db.delete(zakazka)
    db.commit()
    return {"detail": "Smazáno"}
