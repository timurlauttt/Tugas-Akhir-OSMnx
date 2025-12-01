import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

flood = gpd.read_file("data_processed/Data_Desa_Rawan_Banjir_di_Cilacap.geojson")

fig, ax = plt.subplots(figsize=(10, 8))
flood.plot(ax=ax, markersize=50, color="#009E73", marker="o", edgecolor="k", linewidth=1)

legend_handles = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor="#009E73",
           markeredgecolor='k', markersize=10, label="Flood-risk Points")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Flood-risk Points - Kabupaten Cilacap", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()