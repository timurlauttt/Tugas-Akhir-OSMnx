import os
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ox.settings.log_console = True
ox.settings.use_cache = True

area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"

# Ambil jaringan jalan
road = ox.graph_from_place(area, network_type="all")

os.makedirs("data_processed", exist_ok=True)
ox.save_graphml(road, "data_processed/road.graphml")

print(road)

# Konversi graph ke GeoDataFrame untuk plotting manual
nodes, edges = ox.graph_to_gdfs(road)

# Plot dengan warna konsisten (biru untuk roads)
fig, ax = plt.subplots(figsize=(10, 8))
edges.plot(ax=ax, linewidth=0.8, color="#0072B2")

# Legend
legend_handles = [
    Line2D([0], [0], color="#0072B2", lw=1, label="Roads")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow (petunjuk arah mata angin)
nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Roads - Kabupaten Cilacap", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()
