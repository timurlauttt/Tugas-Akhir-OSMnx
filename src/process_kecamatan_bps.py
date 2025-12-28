"""
Process shapefile kecamatan dari BPS
Input: ADMINISTRASI_LN_25K.shp dari Downloads/KAB.CILACAP/
Output: GeoJSON & Shapefile kecamatan Cilacap dengan boundary yang lengkap
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import os
from shapely.ops import unary_union
from shapely.geometry import Polygon, MultiPolygon

# Setup paths
downloads_path = os.path.expanduser('~/Downloads/KAB. CILACAP')
output_dir = 'data_processed'
os.makedirs(output_dir, exist_ok=True)

print("📂 Loading shapefile BPS...")
print(f"   Path: {downloads_path}")

# Load shapefile kecamatan (ADMINISTRASIDESA_AR adalah polygon desa)
shp_path = os.path.join(downloads_path, 'ADMINISTRASIDESA_AR_25K.shp')

if not os.path.exists(shp_path):
    print(f"❌ File tidak ditemukan: {shp_path}")
    print("\nFile yang tersedia di folder:")
    for f in os.listdir(downloads_path):
        print(f"   - {f}")
    exit(1)

# Load shapefile
gdf = gpd.read_file(shp_path)
print(f"✓ Loaded {len(gdf)} features")
print(f"  CRS: {gdf.crs}")
print(f"  Columns: {gdf.columns.tolist()}")

# Tampilkan beberapa contoh data untuk identifikasi kolom
print("\nContoh data (5 baris pertama):")
print(gdf.head())

# Check geometry types
print(f"\nGeometry types: {gdf.geometry.type.value_counts().to_dict()}")

# Reproject ke EPSG:4326 jika perlu
if gdf.crs and gdf.crs != 'EPSG:4326':
    print(f"🔄 Reprojecting from {gdf.crs} to EPSG:4326...")
    gdf = gdf.to_crs('EPSG:4326')
    print("✓ Reprojected")

# Identifikasi kolom kecamatan
# WADMKC = Nama Kecamatan, NAMOBJ = Nama Desa
if 'WADMKC' in gdf.columns:
    print(f"\n📝 Kolom WADMKC (kecamatan) ditemukan")
    print(f"   Jumlah desa: {len(gdf)}")
    print(f"   Jumlah kecamatan unik: {gdf['WADMKC'].nunique()}")
    print(f"\nKecamatan yang ada:")
    for idx, kec in enumerate(sorted(gdf['WADMKC'].unique()), 1):
        count = len(gdf[gdf['WADMKC'] == kec])
        print(f"   {idx:2d}. {kec} ({count} desa)")
    
    # Group by kecamatan dan gabungkan geometries
    print("\n🔄 Menggabungkan desa per kecamatan...")
    kecamatan_gdf = gdf.dissolve(by='WADMKC', as_index=False)
    kecamatan_gdf['kecamatan'] = kecamatan_gdf['WADMKC']
    print(f"✓ Berhasil menggabungkan menjadi {len(kecamatan_gdf)} kecamatan")
else:
    print("\n❌ Kolom WADMKC tidak ditemukan!")
    print(f"Kolom yang tersedia: {gdf.columns.tolist()}")
    exit(1)

# Gunakan kecamatan_gdf untuk processing selanjutnya
gdf = kecamatan_gdf

# Add metadata
gdf['kabupaten'] = 'Cilacap'
gdf['provinsi'] = 'Jawa Tengah'
gdf['sumber'] = 'BPS'

# Filter hanya kolom penting
keep_columns = ['kecamatan', 'kabupaten', 'provinsi', 'sumber', 'geometry']
gdf = gdf[keep_columns].copy()

# Sort by kecamatan
gdf = gdf.sort_values('kecamatan').reset_index(drop=True)

print(f"\n📊 Total kecamatan: {len(gdf)}")
print("\nDaftar kecamatan:")
for idx, name in enumerate(gdf['kecamatan'], 1):
    print(f"  {idx:2d}. {name}")

# Save ke GeoJSON
geojson_path = os.path.join(output_dir, 'kecamatan_cilacap_bps.geojson')
gdf.to_file(geojson_path, driver='GeoJSON')
print(f"\n✅ Saved: {geojson_path}")

# Save ke Shapefile
shp_output = os.path.join(output_dir, 'kecamatan_cilacap_bps.shp')
gdf.to_file(shp_output)
print(f"✅ Saved: {shp_output}")

# Visualisasi
print("\n🎨 Generating visualization...")
fig, ax = plt.subplots(figsize=(16, 18))

# Plot dengan warna berbeda tiap kecamatan
gdf.plot(
    ax=ax,
    column='kecamatan',
    cmap='tab20',
    edgecolor='black',
    linewidth=1.5,
    legend=False
)

# Add labels di centroid atau representative point
for idx, row in gdf.iterrows():
    try:
        # Gunakan representative_point untuk shape kompleks
        if isinstance(row.geometry, (Polygon, MultiPolygon)):
            point = row.geometry.representative_point()
        else:
            point = row.geometry.centroid
        
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
ax.set_title('Peta Kecamatan - Kabupaten Cilacap\n(Data BPS)', 
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

# Legend dengan jumlah
ax.text(0.02, 0.98, f'Total: {len(gdf)} Kecamatan',
        transform=ax.transAxes,
        fontsize=12, fontweight='bold',
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()

# Save visualization
vis_path = os.path.join(output_dir, 'kecamatan_map_bps.png')
plt.savefig(vis_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {vis_path}")

plt.close()

print("\n" + "="*60)
print("✅ SELESAI!")
print(f"   Output: {geojson_path}")
print(f"   Output: {shp_output}")
print(f"   Visualisasi: {vis_path}")
print("="*60)
