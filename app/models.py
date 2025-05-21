from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-many spojovací tabulka pro role
mechanik_role = Table(
    "mechanik_role",
    Base.metadata,
    Column("mechanik_id", Integer, ForeignKey("mechanici.id")),
    Column("role_id", Integer, ForeignKey("role.id")),
)

class Zakaznik(Base):
    __tablename__ = "zakaznici"
    id = Column(Integer, primary_key=True, index=True)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    heslo = Column(String, nullable=False)
    telefon = Column(String)
    adresa = Column(String)
    zakazky = relationship("Zakazka", back_populates="zakaznik")

class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True, index=True)
    nazev = Column(String, unique=True, nullable=False)

class Mechanik(Base):
    __tablename__ = "mechanici"
    id = Column(Integer, primary_key=True, index=True)
    jmeno = Column(String, nullable=False)
    prijmeni = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    heslo = Column(String, nullable=False)
    telefon = Column(String)
    role = relationship("Role", secondary=mechanik_role, backref="mechanici")
    zakazky = relationship("Zakazka", back_populates="mechanik")

class Zakazka(Base):
    __tablename__ = "zakazky"
    id = Column(Integer, primary_key=True, index=True)
    popis = Column(String, nullable=False)
    stav = Column(String, default="otevřená")
    datum_prijmu = Column(Date)
    datum_predani = Column(Date)
    auto_znacka = Column(String)
    auto_model = Column(String)
    auto_vin = Column(String)
    cena = Column(Float)

    zakaznik_id = Column(Integer, ForeignKey("zakaznici.id"))
    mechanik_id = Column(Integer, ForeignKey("mechanici.id"))

    zakaznik = relationship("Zakaznik", back_populates="zakazky")
    mechanik = relationship("Mechanik", back_populates="zakazky")
