import os
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ox.settings.use_cache = True
ox.settings.log_console = False

boundary = gpd.read_file("data_processed/boundary.geojson")
building = gpd.read_file("data_processed/building.geojson")
road = ox.load_graphml("data_processed/road.graphml")
flood_points = gpd.read_file("data_processed/Data_Desa_Rawan_Banjir_di_Cilacap.geojson")
evac_points = gpd.read_file("data_processed/tempatevakuasinew.geojson")

# Filter evakuasi banjir/tsunami
if 'col_12' in evac_points.columns:
    evac_points['jenis_bencana'] = evac_points['col_12'].astype(str).str.lower()
    evac_flood = evac_points[evac_points['jenis_bencana'].str.contains('banjir|tsunami', na=False)]
    evac_other = evac_points[~evac_points['jenis_bencana'].str.contains('banjir|tsunami', na=False)]
else:
    evac_flood = evac_points
    evac_other = gpd.GeoDataFrame()

nodes, edges = ox.graph_to_gdfs(road)

fig, ax = plt.subplots(figsize=(12, 12))

# boundary: tetap hitam (kontras tinggi)
boundary.plot(ax=ax, facecolor="none", edgecolor="#000000", linewidth=2, zorder=4)

# roads: colorblind-friendly blue (kontras baik terhadap boundary)
edges.plot(ax=ax, linewidth=0.8, color="#0072B2", zorder=2)

# buildings: colorblind-friendly vermillion/orange, sedikit tebal dan dengan edge untuk visibilitas
building.plot(ax=ax, color="#D55E00", alpha=0.9, edgecolor="#8B3E00", linewidth=0.3, zorder=3)

# flood points: green circles
flood_points.plot(ax=ax, markersize=30, color="#009E73", marker="o", edgecolor="k", linewidth=1, zorder=5)

# evacuation points: yellow triangles for flood/tsunami, gray for others
if not evac_flood.empty:
    evac_flood.plot(ax=ax, markersize=40, color="#F0E442", marker="^", edgecolor="k", linewidth=1, zorder=6)
if not evac_other.empty:
    evac_other.plot(ax=ax, markersize=30, color="#999999", marker="^", edgecolor="#666666", linewidth=0.8, alpha=0.6, zorder=5)

# Legend (jelaskan warna/layer)
legend_handles = [
    Line2D([0], [0], color="#000000", lw=2, label="Boundary"),
    Line2D([0], [0], color="#0072B2", lw=1, label="Roads"),
    Patch(facecolor="#D55E00", edgecolor="#8B3E00", label="Buildings"),
    Line2D([0], [0], marker='o', color='w', markerfacecolor="#009E73",
           markeredgecolor='k', markersize=8, label=f"Flood-risk Points ({len(flood_points)})"),
    Line2D([0], [0], marker='^', color='w', markerfacecolor="#F0E442",
           markeredgecolor='k', markersize=9, label=f"Evac Flood/Tsunami ({len(evac_flood)})"),
    Line2D([0], [0], marker='^', color='w', markerfacecolor="#999999",
           markeredgecolor='#666666', markersize=7, label=f"Evac Other ({len(evac_other)})")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow (petunjuk arah mata angin)
nx, ny = 0.95, 0.15  # posisinya di axes fraction (ubah jika perlu)
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Layered Map: Boundary + Roads + Buildings + Flood + Evacuation", fontsize=16)
ax.set_axis_off()
plt.tight_layout()

plt.show()
