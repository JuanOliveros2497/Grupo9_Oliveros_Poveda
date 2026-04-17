#!/usr/bin/env python3
import os
import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CountriesExtractor:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL')
        self.fields = os.getenv('FIELDS')

        if not self.base_url or not self.fields:
            raise ValueError("BASE_URL o FIELDS no configurados en .env")

    def extraer_paises(self):
        """Extrae datos de todos los países"""
        try:
            url = f"{self.base_url}/all?fields={self.fields}"

            response = requests.get(url, timeout=15)
            response.raise_for_status()

            data = response.json()

            logger.info(f"✅ Datos extraídos correctamente: {len(data)} países")
            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error en extracción: {str(e)}")
            return []

    def procesar_pais(self, pais):
        """Procesa un país a formato estructurado"""
        try:
            name = pais.get("name", {}).get("common")
            capital = pais.get("capital", [None])[0]
            region = pais.get("region")
            subregion = pais.get("subregion")
            population = pais.get("population")
            area = pais.get("area")
            latlng = pais.get("latlng", [None, None])

            # Calcular densidad
            density = population / area if area and area != 0 else None

            return {
                "name": name,
                "capital": capital,
                "region": region,
                "subregion": subregion,
                "population": population,
                "area": area,
                "latitude": latlng[0],
                "longitude": latlng[1],
                "density": density,
                "fecha_extraccion": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Error procesando país: {str(e)}")
            return None

    def ejecutar_extraccion(self):
        """Ejecuta todo el proceso ETL (extract + transform)"""
        datos_crudos = self.extraer_paises()
        datos_procesados = []

        for pais in datos_crudos:
            registro = self.procesar_pais(pais)
            if registro:
                datos_procesados.append(registro)

        logger.info(f"✅ Total registros procesados: {len(datos_procesados)}")
        return datos_procesados


if __name__ == "__main__":
    try:
        extractor = CountriesExtractor()
        datos = extractor.ejecutar_extraccion()

        # Guardar JSON
        with open('data/countries_raw.json', 'w') as f:
            json.dump(datos, f, indent=2)

        logger.info("📁 Datos guardados en data/countries_raw.json")

        # Guardar CSV
        df = pd.DataFrame(datos)
        df.to_csv('data/countries.csv', index=False)

        logger.info("📁 Datos guardados en data/countries.csv")

        # Mostrar resumen
        print("\n" + "="*50)
        print("RESUMEN DE EXTRACCIÓN")
        print("="*50)
        print(df.head(10))
        print("="*50)

    except Exception as e:
        logger.error(f"❌ Error en ejecución: {str(e)}")
