import os
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ox.settings.log_console = True
ox.settings.use_cache = True

area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"
boundary = ox.geocode_to_gdf(area)

os.makedirs("data_processed", exist_ok=True)
boundary.to_file("data_processed/boundary.geojson", driver="GeoJSON")

print(boundary)

# Plot dengan warna konsisten (hitam untuk boundary)
fig, ax = plt.subplots(figsize=(10, 8))
boundary.plot(ax=ax, facecolor="none", edgecolor="#000000", linewidth=2)

# Legend
legend_handles = [
    Line2D([0], [0], color="#000000", lw=2, label="Boundary")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow (petunjuk arah mata angin)
nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Boundary - Kabupaten Cilacap", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()