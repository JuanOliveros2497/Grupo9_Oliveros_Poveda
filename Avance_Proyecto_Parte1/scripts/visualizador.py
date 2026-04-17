#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("data/paises.csv")

print("Columnas detectadas:", df.columns)

# -------------------------------
# 1️⃣ Monedas más usadas
# -------------------------------

monedas = df["moneda"].value_counts().head(10)

plt.figure(figsize=(10,6))
plt.bar(monedas.index, monedas.values)
plt.title("Monedas más utilizadas")
plt.ylabel("Cantidad de países")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("data/grafica_monedas.png")
print("✅ Guardado: grafica_monedas.png")

# -------------------------------
# 2️⃣ Capitales
# -------------------------------

capitales = df["capital"].value_counts().head(10)

plt.figure(figsize=(10,6))
plt.bar(capitales.index, capitales.values)
plt.title("Capitales registradas")
plt.ylabel("Cantidad")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("data/grafica_capitales.png")
print("✅ Guardado: grafica_capitales.png")

# -------------------------------
# 3️⃣ Top países por población
# -------------------------------

top_poblacion = df.sort_values("poblacion", ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.bar(top_poblacion["pais"], top_poblacion["poblacion"])
plt.title("Top 10 países por población")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("data/grafica_poblacion.png")
print("✅ Guardado: grafica_poblacion.png")

# -------------------------------
# 4️⃣ Área vs población
# -------------------------------

plt.figure(figsize=(10,6))
plt.scatter(df["area"], df["poblacion"])
plt.title("Área vs Población")
plt.xlabel("Área")
plt.ylabel("Población")

plt.tight_layout()
plt.savefig("data/grafica_area_vs_poblacion.png")
print("✅ Guardado: grafica_area_vs_poblacion.png")

print("\n🎉 Todas las gráficas fueron generadas correctamente.")