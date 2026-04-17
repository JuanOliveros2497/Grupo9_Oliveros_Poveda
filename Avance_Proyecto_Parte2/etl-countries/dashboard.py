#!/usr/bin/env python3
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(
    page_title="🌍 Dashboard Países PRO",
    layout="wide"
)

# =========================
# 🔌 CONEXIÓN DB
# =========================
def conectar():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="countries_db",
        user="daniel",
        password="1234"
    )

# =========================
# 📥 CARGA DATOS
# =========================
@st.cache_data
def cargar_datos():
    conn = conectar()
    df = pd.read_sql("SELECT * FROM countries", conn)
    conn.close()
    return df

df = cargar_datos()

# =========================
# 🎛️ SIDEBAR FILTROS
# =========================
st.sidebar.title("🎛️ Filtros")

regiones = st.sidebar.multiselect(
    "🌍 Región",
    options=df['region'].dropna().unique(),
    default=df['region'].dropna().unique()
)

poblacion_min = st.sidebar.slider(
    "👥 Población mínima",
    int(df['population'].min()),
    int(df['population'].max()),
    int(df['population'].min())
)

area_min = st.sidebar.slider(
    "📏 Área mínima",
    int(df['area'].min()),
    int(df['area'].max()),
    int(df['area'].min())
)

df = df[
    (df['region'].isin(regiones)) &
    (df['population'] >= poblacion_min) &
    (df['area'] >= area_min)
]

# =========================
# 🏷️ HEADER
# =========================
st.title("🌍 Dashboard Global de Países")
st.markdown("Análisis interactivo de datos demográficos y geográficos")

# =========================
# 📊 KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🌎 Países", len(df))
col2.metric("👥 Población Total", f"{df['population'].sum():,}")
col3.metric("📏 Área Promedio", f"{df['area'].mean():,.0f}")
col4.metric("📊 Densidad Prom", f"{df['density'].mean():.2f}")

st.markdown("---")

# =========================
# 📑 TABS
# =========================
tab1, tab2, tab3 = st.tabs(["📊 General", "🏆 Rankings", "🗺️ Mapa"])

# =========================
# 📊 TAB 1 - GENERAL
# =========================
with tab1:
    st.subheader("🌍 Distribución por región")

    region_counts = df['region'].value_counts().reset_index()
    region_counts.columns = ['region', 'count']

    fig = px.bar(
        region_counts,
        x='region',
        y='count',
        title="Cantidad de países por región"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("👥 Población por país")

    top20 = df.sort_values(by='population', ascending=False).head(20)

    fig = px.bar(
        top20,
        x='name',
        y='population',
        title="Top 20 países por población"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🏆 TAB 2 - RANKINGS
# =========================
with tab2:
    st.subheader("🏆 Top 10 países más poblados")

    top_pop = df.sort_values(by='population', ascending=False).head(10)

    fig = px.bar(top_pop, x='name', y='population', color='population')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📏 Top 10 países más grandes")

    top_area = df.sort_values(by='area', ascending=False).head(10)

    fig = px.bar(top_area, x='name', y='area', color='area')
    st.plotly_chart(fig, use_container_width=True)

# =========================
# 🗺️ TAB 3 - MAPA
# =========================
with tab3:
    st.subheader("🗺️ Ubicación geográfica")

    mapa_df = df[['latitude', 'longitude']].dropna()

    if not mapa_df.empty:
        st.map(mapa_df)
    else:
        st.warning("No hay coordenadas disponibles")

# =========================
# 📋 TABLA
# =========================
st.markdown("---")
st.subheader("📋 Datos completos")

mostrar_todos = st.checkbox("Mostrar todos los registros")

columnas = st.multiselect(
    "Columnas a mostrar:",
    df.columns.tolist(),
    default=['name', 'capital', 'region', 'population']
)

if mostrar_todos:
    st.dataframe(df[columnas], use_container_width=True)
else:
    st.dataframe(df[columnas].head(20), use_container_width=True)

# =========================
# ⬇️ DESCARGA
# =========================
csv = df.to_csv(index=False)

st.download_button(
    label="⬇️ Descargar datos como CSV",
    data=csv,
    file_name="countries_data.csv",
    mime="text/csv"
)
