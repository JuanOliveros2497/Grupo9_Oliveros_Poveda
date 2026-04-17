def main():
    import streamlit as st
    import pandas as pd
    from sqlalchemy import create_engine
    import os
    from dotenv import load_dotenv

    load_dotenv()

    DB_USER = os.getenv("DB_USER", "etl_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "etl_pass")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "paises_db")

    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    st.title("🌍 Dashboard Completo de Países")

    @st.cache_data(ttl=60)
    def cargar_datos():
        query = "SELECT * FROM paises;"
        return pd.read_sql(query, engine)

    df = cargar_datos()

    st.sidebar.header("Filtros")

    regiones = df["region"].sort_values().unique()
    region_seleccionada = st.sidebar.multiselect(
        "Selecciona regiones:", regiones, default=regiones
    )

    paises = df[df["region"].isin(region_seleccionada)]["pais"].sort_values().unique()
    pais_seleccionado = st.sidebar.multiselect(
        "Selecciona países:", paises, default=paises
    )

    df_filtrado = df[
        (df["region"].isin(region_seleccionada)) &
        (df["pais"].isin(pais_seleccionado))
    ]

    st.subheader("📊 Información general")
    st.metric("Total países", len(df_filtrado))
    st.metric("Total población", int(df_filtrado["poblacion"].sum()))
    st.metric("Total área", round(df_filtrado["area"].sum(), 2))

    st.dataframe(df_filtrado)

    st.subheader("📈 Población por Región")
    st.bar_chart(df_filtrado.groupby("region")["poblacion"].sum())

    st.subheader("🌐 Área por Región")
    st.bar_chart(df_filtrado.groupby("region")["area"].sum())

    st.subheader("💰 Distribución de Monedas")
    st.bar_chart(df_filtrado["moneda"].value_counts())

    st.subheader("🗣 Distribución de Idiomas")
    st.bar_chart(df_filtrado["idioma"].value_counts())


if __name__ == "__main__":
    main()