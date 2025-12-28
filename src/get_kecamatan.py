import os
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUTPUT_DIR = "data_processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Path ke shapefile BPS
BPS_SHAPEFILE = os.path.expanduser('~/Downloads/KAB. CILACAP/ADMINISTRASIDESA_AR_25K.shp')

# Daftar 24 kecamatan resmi Kabupaten Cilacap
kecamatan_list = [
    "Adipala",
    "Bantarsari",
    "Binangun",
    "Cilacap Selatan",
    "Cilacap Tengah",
    "Cilacap Utara",
    "Cimanggu",
    "Cipari",
    "Dayeuhluhur",
    "Gandrungmangu",
    "Jeruklegi",
    "Kampung Laut",
    "Karangpucung",
    "Kawunganten",
    "Kedungreja",
    "Kesugihan",
    "Kroya",
    "Majenang",
    "Maos",
    "Nusawungu",
    "Patimuan",
    "Sampang",
    "Sidareja",
    "Wanareja"
]

print(f"📂 Loading shapefile BPS dari: {BPS_SHAPEFILE}")

# Load shapefile desa
gdf_desa = gpd.read_file(BPS_SHAPEFILE)
print(f"✓ Loaded {len(gdf_desa)} desa")
print(f"  CRS: {gdf_desa.crs}")

# Reproject ke EPSG:4326 jika perlu
if gdf_desa.crs and gdf_desa.crs != 'EPSG:4326':
    print(f"🔄 Reprojecting to EPSG:4326...")
    gdf_desa = gdf_desa.to_crs('EPSG:4326')

# Check kolom WADMKC (Nama Kecamatan)
if 'WADMKC' not in gdf_desa.columns:
    print(f"❌ Kolom WADMKC tidak ditemukan!")
    print(f"Kolom yang tersedia: {gdf_desa.columns.tolist()}")
    exit(1)

print(f"\n🔄 Menggabungkan {len(gdf_desa)} desa menjadi kecamatan...")
# Dissolve desa per kecamatan
kecamatan_gdf = gdf_desa.dissolve(by='WADMKC', as_index=False)
kecamatan_gdf['kecamatan'] = kecamatan_gdf['WADMKC']
kecamatan_gdf['kabupaten'] = 'Cilacap'
kecamatan_gdf['provinsi'] = 'Jawa Tengah'
kecamatan_gdf['sumber'] = 'BPS'

print(f"✓ Berhasil menggabungkan menjadi {len(kecamatan_gdf)} kecamatan")

# Filter hanya 24 kecamatan Cilacap
print(f"\n✂️  Filtering hanya 24 kecamatan Kabupaten Cilacap...")
kecamatan_gdf = kecamatan_gdf[kecamatan_gdf['kecamatan'].isin(kecamatan_list)].copy()
print(f"✓ Hasil filter: {len(kecamatan_gdf)} kecamatan")

# Sort alphabetically
kecamatan_gdf = kecamatan_gdf.sort_values('kecamatan').reset_index(drop=True)

# Keep only important columns
keep_columns = ['kecamatan', 'kabupaten', 'provinsi', 'sumber', 'geometry']
kecamatan_gdf = kecamatan_gdf[keep_columns]

print(f"\n📋 Daftar kecamatan:")
for idx, kec in enumerate(kecamatan_gdf['kecamatan'], 1):
    print(f"   {idx:2d}. {kec}")
    
# Simpan ke GeoJSON
output_path = os.path.join(OUTPUT_DIR, "kecamatan_cilacap.geojson")
kecamatan_gdf.to_file(output_path, driver="GeoJSON")
print(f"\n✅ Saved: {output_path}")
print(f"   Total kecamatan: {len(kecamatan_gdf)}")

# Simpan juga ke Shapefile
shp_path = os.path.join(OUTPUT_DIR, "kecamatan_cilacap.shp")
kecamatan_gdf.to_file(shp_path)
print(f"✅ Saved: {shp_path}")

# Visualisasi
print("\n🎨 Generating visualization...")
fig, ax = plt.subplots(figsize=(16, 18))

# Plot semua kecamatan dengan warna berbeda
kecamatan_gdf.plot(ax=ax, column='kecamatan', cmap='tab20', 
                   edgecolor='black', linewidth=1.5, alpha=0.7, 
                   legend=False)

# Tambahkan label nama kecamatan di representative point
for idx, row in kecamatan_gdf.iterrows():
    try:
        point = row.geometry.representative_point()
        ax.text(point.x, point.y, row['kecamatan'], 
                fontsize=9, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray'))
    except Exception as e:
        print(f"  Warning: Cannot label {row['kecamatan']}")

# Legend
legend_handles = [
    Line2D([0], [0], color='black', lw=2, label=f"Kecamatan ({len(kecamatan_gdf)})")
]
ax.legend(handles=legend_handles, loc="lower left", frameon=True, fontsize=10)

# North arrow
nx, ny = 0.95, 0.15
ax.annotate('', xy=(nx, ny + 0.12), xytext=(nx, ny),
            xycoords='axes fraction',
            arrowprops=dict(facecolor='k', width=2, headwidth=8))
ax.text(nx, ny + 0.135, 'N', transform=ax.transAxes,
        ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title("Peta 24 Kecamatan - Kabupaten Cilacap\n(Data BPS)", 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

plt.tight_layout()

# Save visualization
viz_path = os.path.join(OUTPUT_DIR, "kecamatan_map.png")
plt.savefig(viz_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved visualization: {viz_path}")

plt.close()

print("\n" + "="*60)
print("✅ SELESAI!")
print(f"   {len(kecamatan_gdf)} kecamatan berhasil diproses dari data BPS")
print(f"   Output: {output_path}")
print(f"   Shapefile: {shp_path}")
print(f"   Visualisasi: {viz_path}")
print("="*60)
plt.show()