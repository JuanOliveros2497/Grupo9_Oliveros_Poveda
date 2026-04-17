#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Cargar datos
df = pd.read_csv('data/countries.csv')

# Limpiar datos (evitar nulos)
df = df.dropna(subset=['population', 'area', 'density'])

# Top 10 países más poblados
top_poblacion = df.sort_values(by='population', ascending=False).head(10)

# Top 10 países más grandes (área)
top_area = df.sort_values(by='area', ascending=False).head(10)

# Top 10 países más densos
top_density = df.sort_values(by='density', ascending=False).head(10)

# Agrupación por región
region_data = df.groupby('region')['population'].sum().sort_values(ascending=False)

# Crear figura
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Análisis Global de Países', fontsize=16, fontweight='bold')

# Gráfica 1: Top población
ax1 = axes[0, 0]
ax1.bar(top_poblacion['name'], top_poblacion['population'])
ax1.set_title('Top 10 Países por Población')
ax1.set_ylabel('Población')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Gráfica 2: Top área
ax2 = axes[0, 1]
ax2.bar(top_area['name'], top_area['area'])
ax2.set_title('Top 10 Países por Área')
ax2.set_ylabel('Área (km²)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Gráfica 3: Densidad poblacional
ax3 = axes[1, 0]
ax3.scatter(top_density['name'], top_density['density'], s=100)
ax3.set_title('Top 10 Países por Densidad')
ax3.set_ylabel('Densidad (hab/km²)')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(alpha=0.3)

# Gráfica 4: Población por región
ax4 = axes[1, 1]
ax4.bar(region_data.index, region_data.values)
ax4.set_title('Población Total por Región')
ax4.set_ylabel('Población')
ax4.tick_params(axis='x', rotation=45)
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('data/countries_analysis.png', dpi=300, bbox_inches='tight')
logger.info("✅ Gráficas guardadas en data/countries_analysis.png")

plt.show()
