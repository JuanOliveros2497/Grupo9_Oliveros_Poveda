import pandas as pd
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "database": "countries_db",
    "user": "daniel",
    "password": "1234"
}

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def insertar_datos():
    try:
        conn = conectar()
        cur = conn.cursor()

        df = pd.read_csv("data/countries.csv")

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO countries (
                    name, capital, region, subregion,
                    population, area, latitude, longitude,
                    density, fecha_extraccion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['name'],
                row['capital'],
                row['region'],
                row['subregion'],
                row['population'],
                row['area'],
                row['latitude'],
                row['longitude'],
                row['density'],
                row['fecha_extraccion']
            ))

        conn.commit()
        cur.close()
        conn.close()

        logger.info("✅ Datos insertados correctamente")

    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == "__main__":
    insertar_datos()
