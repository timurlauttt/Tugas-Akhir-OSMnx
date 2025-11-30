import os
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ox.settings.log_console = True
ox.settings.use_cache = True

area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"

# Ambil semua fitur bangunan
building = ox.features_from_place(
    area,
    tags={"building": True}
)

os.makedirs("data_processed", exist_ok=True)
building.to_file("data_processed/building.geojson", driver="GeoJSON")

print(building)

# Plot dengan warna konsisten (vermillion/orange untuk buildings)
fig, ax = plt.subplots(figsize=(10, 8))
building.plot(ax=ax, color="#D55E00", alpha=0.9, edgecolor="#8B3E00", linewidth=0.3)

# Legend
legend_handles = [
    Patch(facecolor="#D55E00", edgecolor="#8B3E00", label="Buildings")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow (petunjuk arah mata angin)
nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Buildings - Kabupaten Cilacap", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()
