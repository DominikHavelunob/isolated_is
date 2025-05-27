from sqlalchemy import Column, String, Date, Float, ForeignKey, Boolean, Text, Table, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime
from .database import Base


class Admin(Base):
    __tablename__ = "admini"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    heslo = Column(String, nullable=False)


mechanik_role = Table(
    "mechanik_role",
    Base.metadata,
    Column("mechanik_id", UUID(as_uuid=True), ForeignKey("mechanici.id")),
    Column("role_id", UUID(as_uuid=True), ForeignKey("role.id")),
)

class Zakaznik(Base):
    __tablename__ = "zakaznici"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    heslo = Column(String, nullable=False)
    telefon = Column(String)
    adresa = Column(String)
    anonymizovan = Column(Boolean, default=False)
    smazano = Column(Boolean, default=False)
    zakazky = relationship("Zakazka", back_populates="zakaznik")


class Role(Base):
    __tablename__ = "role"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nazev = Column(String, unique=True, nullable=False)
    mechanici = relationship(
        "Mechanik", secondary=mechanik_role, back_populates="role"
    )

class Mechanik(Base):
    __tablename__ = "mechanici"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    heslo = Column(String, nullable=False)
    telefon = Column(String)
    role = relationship("Role", secondary="mechanik_role", back_populates="mechanici")
    zakazky = relationship("Zakazka", back_populates="mechanik")

class LogZakazky(Base):
    __tablename__ = "logy_zakazek"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    zakazka_id = Column(UUID(as_uuid=True), ForeignKey("zakazky.id"))
    provedl_id = Column(UUID(as_uuid=True))
    akce = Column(String)
    popis = Column(Text)
    datum = Column(DateTime, default=datetime.utcnow)

class Zakazka(Base):
    __tablename__ = "zakazky"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    popis = Column(String, nullable=False)
    stav = Column(String, default="otevřená")
    hotova = Column(Boolean, default=False)
    datum_prijmu = Column(Date)
    datum_predani = Column(Date)
    auto_znacka = Column(String)
    auto_model = Column(String)
    auto_vin = Column(String)
    cena = Column(Float)
    anonymizovana = Column(Boolean, default=False)
    smazano = Column(Boolean, default=False)

    zakaznik_id = Column(UUID(as_uuid=True), ForeignKey("zakaznici.id"))
    mechanik_id = Column(UUID(as_uuid=True), ForeignKey("mechanici.id"))
#    vytvoril_id = Column(UUID(as_uuid=True), ForeignKey("admini.id"), nullable=True)
    vytvoril_id = Column(UUID(as_uuid=True), nullable=True)

    zakaznik = relationship("Zakaznik", back_populates="zakazky")
    mechanik = relationship("Mechanik", back_populates="zakazky")
