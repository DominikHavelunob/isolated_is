from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date






# ==== Role ====
class RoleBase(BaseModel):
    nazev: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    class Config:
        orm_mode = True

# ==== Role ====




# ==== Mechanik ====
class MechanikBase(BaseModel):
    jmeno: str
    prijmeni: str
    email: EmailStr
    telefon: Optional[str]

class MechanikCreate(BaseModel):
    jmeno: str
    prijmeni: str
    heslo: str
    telefon: Optional[str]
    role_ids: List[int] = []

class Mechanik(MechanikBase):
    id: int
    # pripadna zmena na role: List[Role] = []
    role: List["Role"] = []
    class Config:
        orm_mode = True

# ==== Mechanik ====






# ==== Zakaznik ====
class ZakaznikBase(BaseModel):
    jmeno: str
    prijmeni: str
    email: EmailStr
    telefon: Optional[str]
    adresa: Optional[str]

class ZakaznikCreate(ZakaznikBase):
    heslo: str

class Zakaznik(ZakaznikBase):
    id: int
    class Config:
        orm_mode = True

# ==== Zakaznik ====




# ==== Zakazka ====
class ZakazkaBase(BaseModel):
    popis: str
    stav: Optional[str] = "otevřená"
    datum_prijmu: Optional[date]
    datum_predani: Optional[date]
    auto_znacka: Optional[str]
    auto_model: Optional[str]
    auto_vin: Optional[str]
    cena: Optional[float]
    zakaznik_id: int
    mechanik_id: int

class ZakazkaCreate(ZakazkaBase):
    pass

class Zakazka(ZakazkaBase):
    id: int
    class Config:
        orm_mode = True

# ==== Zakazka ====



# ==== Token ====
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    typ_uzivatele: Optional[str] = None

# ==== Token ====