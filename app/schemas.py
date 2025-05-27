from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import date, datetime

# --- ADMIN ---
class AdminBase(BaseModel):
    jmeno: str
    prijmeni: str
    email: EmailStr

class AdminCreate(AdminBase):
    heslo: str

class Admin(AdminBase):
    id: UUID

    class Config:
        from_attributes = True


# --- ROLE ---
class RoleBase(BaseModel):
    nazev: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: UUID

    class Config:
        from_attributes = True


# --- MECHANIK ---
class MechanikBase(BaseModel):
    jmeno: str
    prijmeni: str
    email: EmailStr
    telefon: Optional[str] = None

class MechanikCreate(MechanikBase):
    heslo: str
    role_ids: Optional[List[UUID]] = []

class MechanikUpdate(MechanikBase):
    heslo: Optional[str] = None
    role_ids: Optional[List[UUID]] = []

class Mechanik(MechanikBase):
    id: UUID
    role: List[Role] = []

    class Config:
        from_attributes = True


# --- ZAKAZNIK ---
class ZakaznikBase(BaseModel):
    jmeno: str
    prijmeni: str
    email: EmailStr
    telefon: Optional[str] = None
    adresa: Optional[str] = None

class ZakaznikCreate(ZakaznikBase):
    heslo: str

class ZakaznikUpdate(ZakaznikBase):
    heslo: Optional[str] = None

class Zakaznik(ZakaznikBase):
    id: UUID
    anonymizovan: bool
    smazano: bool

    class Config:
        from_attributes = True


# --- ZAKAZKA ---
class ZakazkaBase(BaseModel):
    popis: str
    stav: Optional[str] = "otevřená"
    hotova: Optional[bool] = False
    datum_prijmu: Optional[date] = None
    datum_predani: Optional[date] = None
    auto_znacka: Optional[str] = None
    auto_model: Optional[str] = None
    auto_vin: Optional[str] = None
    cena: Optional[float] = None

class ZakazkaCreate(ZakazkaBase):
    zakaznik_id: UUID
    mechanik_id: Optional[UUID] = None
    vytvoril_id: Optional[UUID] = None

class ZakazkaUpdate(BaseModel):
    popis: Optional[str] = None
    stav: Optional[str] = None
    hotova: Optional[bool] = None
    datum_prijmu: Optional[date] = None
    datum_predani: Optional[date] = None
    auto_znacka: Optional[str] = None
    auto_model: Optional[str] = None
    auto_vin: Optional[str] = None
    cena: Optional[float] = None
    anonymizovana: Optional[bool] = None
    smazano: Optional[bool] = None
    zakaznik_id: Optional[UUID] = None
    mechanik_id: Optional[UUID] = None
    vytvoril_id: Optional[UUID] = None

    class Config:
        orm_mode = True

class Zakazka(ZakazkaBase):
    id: UUID
    anonymizovana: bool
    smazano: bool
    zakaznik_id: UUID
    mechanik_id: UUID
    vytvoril_id: Optional[UUID] = None

    class Config:
        from_attributes = True

# --- LOGY ZAKAZKY ---
class LogZakazkyBase(BaseModel):
    akce: str
    popis: Optional[str] = None

class LogZakazkyCreate(LogZakazkyBase):
    zakazka_id: UUID
    provedl_id: UUID

class LogZakazky(LogZakazkyBase):
    id: UUID
    zakazka_id: UUID
    provedl_id: UUID
    datum: datetime

    class Config:
        from_attributes = True

# --- TOKENY (pro autentizaci) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
    typ_uzivatele: Optional[str] = None

