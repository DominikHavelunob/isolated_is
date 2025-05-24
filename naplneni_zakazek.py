import random
import psycopg2
from faker import Faker
from datetime import timedelta

fake = Faker()

# Realistické značky a modely
auta = {
    "BMW": ["E46", "E90", "F30", "X5", "X3"],
    "Škoda": ["Octavia", "Superb", "Kodiaq"],
    "Volkswagen": ["Golf", "Passat", "Tiguan"],
    "Audi": ["A3", "A4", "Q5"],
    "Ford": ["Focus", "Mondeo", "Kuga"]
}

# Připojení k databázi
conn = psycopg2.connect(
    dbname="autoservis_db",
    user="postgres",
    password="password",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Načteme ID zákazníků a mechaniků
cur.execute("SELECT id FROM zakaznici")
zakaznici_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM mechanici")
mechanici_ids = [row[0] for row in cur.fetchall()]

# Vytvoření 100 náhodných zakázek
for _ in range(100):
    znacka = random.choice(list(auta.keys()))
    model = random.choice(auta[znacka])
    vin = fake.unique.bothify(text='???######????####')
    cena = round(random.uniform(2000, 50000), 2)
    datum_prijmu = fake.date_between(start_date='-60d', end_date='today')
    datum_predani = datum_prijmu + timedelta(days=random.randint(1, 14))
    popis = random.choice([
        "Výměna oleje a filtrů", "Oprava brzd", "Diagnostika motoru",
        "Výměna spojky", "Příprava na STK", "Geometrie kol"
    ])
    stav = random.choice(["čeká", "probíhá", "hotovo"])

    zakaznik_id = random.choice(zakaznici_ids)
    mechanik_id = random.choice(mechanici_ids)

    cur.execute("""
        INSERT INTO zakazky (
            popis, stav, datum_prijmu, datum_predani,
            auto_znacka, auto_model, auto_vin, cena,
            zakaznik_id, mechanik_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (popis, stav, datum_prijmu, datum_predani,
          znacka, model, vin, cena, zakaznik_id, mechanik_id))

# Uložení a uzavření spojení
conn.commit()
cur.close()
conn.close()
