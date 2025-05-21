Autoservis IS – Backend

Jednoduché FastAPI REST API pro správu autoservisu (zakázky, mechanici s rolemi, zákazníci, autentizace).

========================
SPUŠTĚNÍ PROJEKTU
Nainstaluj závislosti:
pip install -r requirements.txt

Nastav proměnné v .env
(Viz příklad v kořenovém adresáři: název DB, uživatel, heslo.)

Inicializuj migrace a databázi:
alembic init alembic
(Pokud už složka alembic existuje, tento krok přeskoč.)

V souboru alembic/env.py nastav správný import Base:
from app.models import Base
target_metadata = Base.metadata

Vygeneruj první migraci:
alembic revision --autogenerate -m "vytvoreni tabulek"
alembic upgrade head

(Doporučeno) Vlož základní role do tabulky role – například přes SQL:
INSERT INTO role (nazev) VALUES
('Motor'),
('Řídící jednotky'),
('Závěsy'),
('Geometrie');

Přidej prvního mechanika ručně do DB (admin):
Buď přes SQL, nebo použij endpoint /auth/registrace/mechanik. (Dbej na hashování hesla, jinak přihlášení nebude fungovat.)

Spusť backend:
uvicorn app.main:app --reload

Ověř funkčnost v prohlížeči nebo Postmanu:
http://localhost:8000/docs
http://localhost:8000/redoc

========================
DŮLEŽITÉ POZNÁMKY
Složka s routami má být app/routers/, nikoli routes/!

Pokud ti nejde přihlášení, zkontroluj, že heslo je hashované (bcrypt).

Při každé změně modelu proveď novou migraci:
alembic revision --autogenerate -m "popis_zmeny"
alembic upgrade head

========================
ZÁKLADNÍ ENDPOINTY
/auth/prihlaseni – login pro mechaniky i zákazníky (JWT)

/auth/registrace/mechanik – admin registrace mechanika

/auth/registrace/zakaznik – registrace zákazníka

/mechanici, /zakaznici, /zakazky – CRUD operace

========================
