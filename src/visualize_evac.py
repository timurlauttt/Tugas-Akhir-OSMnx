import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

evac = gpd.read_file("data_processed/tempatevakuasinew.geojson")

# Kolom 12 berisi jenis bencana (col_12 setelah rename di get_evac_point.py)
# Filter: cek apakah string mengandung keyword "banjir" atau "tsunami" (case-insensitive)
if 'col_12' in evac.columns:
    evac['jenis_bencana'] = evac['col_12'].astype(str).str.lower()
    evac['is_flood_tsunami'] = evac['jenis_bencana'].str.contains('banjir|tsunami', na=False)
else:
    # fallback jika tidak ada kolom jenis bencana
    evac['is_flood_tsunami'] = True

# Pisahkan GeoDataFrame berdasarkan jenis bencana
evac_flood = evac[evac['is_flood_tsunami'] == True]
evac_other = evac[evac['is_flood_tsunami'] == False]

fig, ax = plt.subplots(figsize=(10, 8))

# Plot evakuasi banjir/tsunami dengan warna kuning (prioritas)
if not evac_flood.empty:
    evac_flood.plot(ax=ax, markersize=70, color="#F0E442", marker="^", 
                    edgecolor="k", linewidth=1.5, zorder=3, label="Flood/Tsunami")

# Plot evakuasi bencana lain dengan warna abu-abu (sekunder)
if not evac_other.empty:
    evac_other.plot(ax=ax, markersize=50, color="#999999", marker="^", 
                   edgecolor="#666666", linewidth=1, alpha=0.6, zorder=2, label="Other Disasters")

# Legend
legend_handles = [
    Line2D([0], [0], marker='^', color='w', markerfacecolor="#F0E442",
           markeredgecolor='k', markersize=12, label=f"Flood/Tsunami Evac ({len(evac_flood)})"),
    Line2D([0], [0], marker='^', color='w', markerfacecolor="#999999",
           markeredgecolor='#666666', markersize=10, label=f"Other Disasters ({len(evac_other)})")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow
nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Evacuation Points - Kabupaten Cilacap", fontsize=14)
ax.set_axis_off()
plt.tight_layout()
plt.show()

# Print summary
print(f"\nSummary:")
print(f"  Flood/Tsunami evacuation points: {len(evac_flood)}")
print(f"  Other disaster evacuation points: {len(evac_other)}")
print(f"  Total: {len(evac)}")