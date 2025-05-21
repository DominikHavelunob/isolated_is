from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError,jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
# OAuth2PasswordBearer neni OAuth2AuthorizationCodeBearer !!!
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
import os



from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# zkouska o2auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/prihlaseni")
# ====
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
    
    if typ_uzivatele == "mechanik":
        user = db.query(models.Mechanik).filter(models.Mechanik.email == email).first()
    elif typ_uzivatele == "zakaznik":
        user = db.query(models.Zakaznik).filter(models.Zakaznik.email == email).first()
    else:
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return user, typ_uzivatele


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
