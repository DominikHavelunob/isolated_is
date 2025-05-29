from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# OAuth2PasswordBearer neni OAuth2AuthorizationCodeBearer !!!
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import logging
from app.database import SessionLocal
from app.models import LogZakazky
from datetime import datetime
import uuid
import os



from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/prihlaseni")

general_exception = HTTPException(status_code=400, detail="BAD REQUEST")

credential_exception = HTTPException(status_code=401, detail="Neuatorizovany uzivatel")

user_exception = HTTPException(status_code=403, detail="Nepovoleny uzivatel")

item_not_found_exception = HTTPException(status_code=404, detail="Polozka nenalezena")



def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Neplatny token",
        headers={"WWW-Authenticate": "Bearer"}
        # validity exception???? 
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        typ_uzivatele: str = payload.get("typ_uzivatele")
        if email is None or typ_uzivatele is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if typ_uzivatele == "admin":
        user = db.query(models.Admin).filter(models.Admin.email == email).first()
    elif typ_uzivatele == "mechanik":
        user = db.query(models.Mechanik).filter(models.Mechanik.email == email).first()
    elif typ_uzivatele == "zakaznik":
        user = db.query(models.Zakaznik).filter(models.Zakaznik.email == email).first()
    else:
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user, typ_uzivatele

def over_vedouciho_mechanika(current=Depends(get_current_user)) -> bool:
    user, typ = current
    if typ != "mechanik":
        raise user_exception
    role_nazvy = [r.nazev for r in user.role]
    if "vedouci_mechanik" in role_nazvy:
        return True
    return False
    

def minimalni_heslo(heslo: str) -> bool:
    if heslo.__len__() > 8:
        if any(char.isdigit() for char in heslo):
            return True
    return False


def hash_heslo(heslo: str) -> str:
    return pwd_context.hash(heslo)

def over_heslo(heslo_plain: str, heslo_hash: str) -> bool:
    return pwd_context.verify(heslo_plain, heslo_hash)

def vytvor_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def je_admin(current=Depends(get_current_user)) -> bool:
    typ = current[1]
    if typ == "admin":
        return True
    return False 

def vyzaduje_admina(current=Depends(get_current_user)):
    if not je_admin(current):
        raise user_exception
    return current[0]

def je_vedouci_mechanik(current=Depends(get_current_user)) -> bool:
    user, typ = current
    if typ == "mechanik":
        return any(r.nazev == "vedouci_mechanik" for r in user.role)
    return False

def vyzaduje_vedouciho_mechanika(current=Depends(get_current_user)):
    if not je_vedouci_mechanik(current):
        raise user_exception
    return current[0] 

def vyzaduje_mechanika(current=Depends(get_current_user)):
    user, typ = current
    if typ == "mechanik":
        return user
    raise user_exception


def vyzaduje_vlastnika_uctu(user_id: int, current=Depends(get_current_user)):
    user = current[0]
    if je_admin(current) or user.id == user_id:
        return user
    raise user_exception


def je_zakaznik(current=Depends(get_current_user)) -> bool:
    typ = current[1]
    if typ == "zakaznik":
        return True
    return False 

def je_mechanik(current=Depends(get_current_user)) -> bool:
    if current[1] == "mechanik":
        return True
    return False



class ZakazkaLogHandler(logging.Handler):
    def emit(self, record):
        session = SessionLocal()
        try:
            log_entry = LogZakazky(
                id=uuid.uuid4(),
                zakazka_id=getattr(record, "zakazka_id", None),
                provedl_id=getattr(record, "provedl_id", None),
                akce=getattr(record, "akce", record.levelname),  # např. "vytvoreni", "uprava"...
                popis=record.getMessage(),
                datum=datetime.utcnow()
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
        finally:
            session.close()

zakazka_logger = logging.getLogger("zakazka_logger")
zakazka_logger.setLevel(logging.INFO)

db_handler = ZakazkaLogHandler()
zakazka_logger.addHandler(db_handler)