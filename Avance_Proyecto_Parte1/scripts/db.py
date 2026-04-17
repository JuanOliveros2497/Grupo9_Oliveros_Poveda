# db.py
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ----------------------------
# Cargar variables de entorno
# ----------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER", "etl_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "etl_pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "paises_db")

# ----------------------------
# Crear engine de SQLAlchemy
# ----------------------------
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=False)

# ----------------------------
# Crear tabla si no existe
# ----------------------------
def crear_tabla():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS paises (
                id SERIAL PRIMARY KEY,
                pais TEXT,
                capital TEXT,
                region TEXT,
                subregion TEXT,
                poblacion BIGINT,
                area DOUBLE PRECISION,
                moneda TEXT,
                idioma TEXT,
                fecha_extraccion TIMESTAMP
            )
        """))

# ----------------------------
# Guardar datos en PostgreSQL
# ----------------------------
def guardar_en_db(lista_datos):
    if not lista_datos:
        return

    stmt = text("""
        INSERT INTO paises (pais, capital, region, subregion, poblacion, area, moneda, idioma, fecha_extraccion)
        VALUES (:pais, :capital, :region, :subregion, :poblacion, :area, :moneda, :idioma, :fecha_extraccion)
    """)

    # Inserción masiva: lista de diccionarios
    with engine.begin() as conn:
        conn.execute(stmt, lista_datos)