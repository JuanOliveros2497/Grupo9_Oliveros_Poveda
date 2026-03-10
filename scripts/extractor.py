#!/usr/bin/env python3
import os
import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import logging

# ----------------------------
# Cargar variables de entorno
# ----------------------------
load_dotenv()

# Crear carpetas
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ----------------------------
# Configuración de logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class RestCountriesExtractor:

    def __init__(self):

        self.base_url = os.getenv("RESTCOUNTRIES_BASE_URL")
        self.timeout = int(os.getenv("REQUEST_TIMEOUT", 10))

        if not self.base_url:
            raise ValueError("❌ RESTCOUNTRIES_BASE_URL no configurada en .env")

    # ----------------------------
    # EXTRACT
    # ----------------------------
    def extraer_paises(self):

        try:

            url = f"{self.base_url}/all?fields=name,capital,currencies,region,subregion,population,area,languages"

            logger.info("🌍 Conectando con la API...")

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            logger.info(f"✅ {len(data)} países extraídos correctamente")

            return data

        except Exception as e:

            logger.error(f"❌ Error extrayendo datos: {str(e)}")
            return []

    # ----------------------------
    # TRANSFORM
    # ----------------------------
    def procesar_respuesta(self, data):

        datos_procesados = []

        for pais in data:

            try:

                nombre = pais.get("name", {}).get("common")

                capital = (
                    pais["capital"][0]
                    if pais.get("capital")
                    else "N/A"
                )

                region = pais.get("region", "N/A")
                subregion = pais.get("subregion", "N/A")

                poblacion = pais.get("population", 0)
                area = pais.get("area", 0)

                moneda = (
                    next(iter(pais.get("currencies", {})), "N/A")
                )

                idioma = (
                    next(iter(pais.get("languages", {}).values()), "N/A")
                )

                registro = {
                    "pais": nombre,
                    "capital": capital,
                    "region": region,
                    "subregion": subregion,
                    "poblacion": poblacion,
                    "area": area,
                    "moneda": moneda,
                    "idioma": idioma,
                    "fecha_extraccion": datetime.now().isoformat()
                }

                datos_procesados.append(registro)

            except Exception as e:

                logger.warning(f"⚠ País omitido: {str(e)}")

        logger.info(f"✅ {len(datos_procesados)} países procesados")

        return datos_procesados

    # ----------------------------
    # PIPELINE
    # ----------------------------
    def ejecutar_extraccion(self):

        logger.info("🚀 Iniciando ETL...")

        raw_data = self.extraer_paises()

        if not raw_data:

            logger.warning("⚠ No se recibieron datos")
            return []

        return self.procesar_respuesta(raw_data)


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    try:

        extractor = RestCountriesExtractor()

        datos = extractor.ejecutar_extraccion()

        if not datos:
            logger.warning("⚠ No hay datos para guardar")
            exit()

        # Guardar JSON
        with open("data/paises_raw.json", "w", encoding="utf-8") as f:

            json.dump(datos, f, indent=2, ensure_ascii=False)

        logger.info("📁 JSON guardado en data/paises_raw.json")

        # Guardar CSV
        df = pd.DataFrame(datos)

        df.to_csv("data/paises.csv", index=False, encoding="utf-8")

        logger.info("📁 CSV guardado en data/paises.csv")

        print("\n" + "="*60)
        print("RESUMEN DE EXTRACCIÓN")
        print("="*60)

        print(df.head(20))

        print("\nColumnas disponibles:")
        print(df.columns)

        print("\nTotal países:", len(df))

        print("="*60)

    except Exception as e:

        logger.error(f"❌ Error en el ETL: {str(e)}")