"""
Filter hanya 24 kecamatan yang termasuk Kabupaten Cilacap
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Daftar 24 kecamatan resmi Kabupaten Cilacap
KECAMATAN_CILACAP = [
    'Adipala', 'Bantarsari', 'Binangun', 'Cilacap Selatan', 'Cilacap Tengah',
    'Cilacap Utara', 'Cimanggu', 'Cipari', 'Dayeuhluhur', 'Gandrungmangu',
    'Jeruklegi', 'Kampung Laut', 'Karangpucung', 'Kawunganten', 'Kedungreja',
    'Kesugihan', 'Kroya', 'Majenang', 'Maos', 'Nusawungu', 'Patimuan',
    'Sampang', 'Sidareja', 'Wanareja'
]

print("🔄 Loading data BPS...")
gdf = gpd.read_file('data_processed/kecamatan_cilacap_bps.geojson')
print(f"   Total kecamatan di file: {len(gdf)}")

# Filter hanya 24 kecamatan Cilacap
print(f"\n✂️  Filtering hanya 24 kecamatan Kabupaten Cilacap...")
gdf_filtered = gdf[gdf['kecamatan'].isin(KECAMATAN_CILACAP)].copy()
print(f"   Hasil filter: {len(gdf_filtered)} kecamatan")

# Check kecamatan yang hilang
missing = set(KECAMATAN_CILACAP) - set(gdf_filtered['kecamatan'])
if missing:
    print(f"\n⚠️  Kecamatan yang tidak ditemukan di data BPS:")
    for kec in sorted(missing):
        print(f"      - {kec}")

# Check kecamatan yang ditemukan
print(f"\n✓ Kecamatan yang ditemukan ({len(gdf_filtered)}):")
for idx, kec in enumerate(sorted(gdf_filtered['kecamatan']), 1):
    print(f"   {idx:2d}. {kec}")

# Sort alphabetically
gdf_filtered = gdf_filtered.sort_values('kecamatan').reset_index(drop=True)

# Save filtered data
output_dir = 'data_processed'
geojson_path = os.path.join(output_dir, 'kecamatan_cilacap_24.geojson')
gdf_filtered.to_file(geojson_path, driver='GeoJSON')
print(f"\n✅ Saved: {geojson_path}")

shp_path = os.path.join(output_dir, 'kecamatan_cilacap_24.shp')
gdf_filtered.to_file(shp_path)
print(f"✅ Saved: {shp_path}")

# Visualisasi
print("\n🎨 Generating visualization...")
fig, ax = plt.subplots(figsize=(16, 18))

gdf_filtered.plot(
    ax=ax,
    column='kecamatan',
    cmap='tab20',
    edgecolor='black',
    linewidth=1.5,
    legend=False
)

# Add labels
for idx, row in gdf_filtered.iterrows():
    try:
        point = row.geometry.representative_point()
        ax.text(
            point.x, point.y,
            row['kecamatan'],
            fontsize=9,
            ha='center',
            va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray')
        )
    except Exception as e:
        print(f"  Warning: Cannot label {row['kecamatan']}: {e}")

# Styling
ax.set_title('Peta 24 Kecamatan - Kabupaten Cilacap\n(Data BPS)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# North arrow
x, y = 0.95, 0.95
ax.annotate('N', xy=(x, y), xytext=(x, y-0.08),
            xycoords='axes fraction',
            fontsize=20, fontweight='bold',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))

# Legend
ax.text(0.02, 0.98, f'Jumlah Kecamatan: {len(gdf_filtered)}',
        transform=ax.transAxes,
        fontsize=12, fontweight='bold',
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()

vis_path = os.path.join(output_dir, 'kecamatan_map_24.png')
plt.savefig(vis_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {vis_path}")

plt.close()

print("\n" + "="*60)
print("✅ SELESAI!")
print(f"   {len(gdf_filtered)} dari 24 kecamatan berhasil diproses")
if missing:
    print(f"   {len(missing)} kecamatan tidak ditemukan di data BPS")
print("="*60)
