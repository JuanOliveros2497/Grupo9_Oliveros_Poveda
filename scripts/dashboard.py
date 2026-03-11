# scripts/dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import os
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
# Conectar a PostgreSQL
# ----------------------------
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ----------------------------
# Título del dashboard
# ----------------------------
st.title("🌍 Dashboard Completo de Países")

# ----------------------------
# Cargar datos con cache para actualizar cada 60s
# ----------------------------
@st.cache_data(ttl=60)
def cargar_datos():
    query = "SELECT * FROM paises;"
    df = pd.read_sql(query, engine)
    return df

df = cargar_datos()

# ----------------------------
# Panel lateral para filtros
# ----------------------------
st.sidebar.header("Filtros")

# Filtrar por región
regiones = df["region"].sort_values().unique()
region_seleccionada = st.sidebar.multiselect("Selecciona regiones:", regiones, default=regiones)

# Filtrar por país
paises = df[df["region"].isin(region_seleccionada)]["pais"].sort_values().unique()
pais_seleccionado = st.sidebar.multiselect("Selecciona países:", paises, default=paises)

# Aplicar filtros
df_filtrado = df[(df["region"].isin(region_seleccionada)) & (df["pais"].isin(pais_seleccionado))]

# ----------------------------
# Información general
# ----------------------------
st.subheader("📊 Información general")
st.metric("Total países", len(df_filtrado))
st.metric("Total población", int(df_filtrado["poblacion"].sum()))
st.metric("Total área", round(df_filtrado["area"].sum(), 2))

st.dataframe(df_filtrado)

# ----------------------------
# Gráficos
# ----------------------------
st.subheader("📈 Población por Región")
poblacion_region = df_filtrado.groupby("region")["poblacion"].sum().sort_values(ascending=False)
st.bar_chart(poblacion_region)

st.subheader("🌐 Área por Región")
area_region = df_filtrado.groupby("region")["area"].sum().sort_values(ascending=False)
st.bar_chart(area_region)

st.subheader("💰 Distribución de Monedas")
moneda_counts = df_filtrado["moneda"].value_counts()
st.bar_chart(moneda_counts)

st.subheader("🗣 Distribución de Idiomas")
idioma_counts = df_filtrado["idioma"].value_counts()
st.bar_chart(idioma_counts)