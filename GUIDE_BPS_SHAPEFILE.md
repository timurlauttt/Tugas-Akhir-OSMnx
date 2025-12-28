# Guide: Download Shapefile Kecamatan dari BPS/Geospasial

## Masalah
OSM (OpenStreetMap) tidak memiliki data boundary lengkap untuk semua 24 kecamatan di Kabupaten Cilacap. Dari percobaan:
- Geocoding by name: **13/24 berhasil** (11 gagal)
- Admin_level query: Mendapat 393 subdivisi (RW/Dusun), bukan kecamatan utama

## Solusi: Shapefile Resmi BPS

### Opsi 1: Portal Geospasial Indonesia (RESMI & GRATIS)
**Website:** https://tanahair.indonesia.go.id/portal-web/

**Langkah:**
1. Buka https://tanahair.indonesia.go.id/portal-web/
2. Menu **"Data"** → **"Data Rupabumi"**
3. Cari: **"Batas Administrasi Kecamatan"** atau **"Administrative Boundary District"**
4. Filter provinsi: **Jawa Tengah** → Kabupaten: **Cilacap**
5. Download format **Shapefile (.shp)** atau **GeoJSON**
6. Extract ke folder `data_raw/`

### Opsi 2: Portal Data Indonesia
**Website:** https://data.go.id/

**Langkah:**
1. Buka https://data.go.id/
2. Search: **"Batas Administrasi Kecamatan Cilacap"**
3. Download dataset dari BPS atau Kementerian Dalam Negeri
4. Extract ke `data_raw/`

### Opsi 3: Langsung dari BPS
**Website:** https://www.bps.go.id/

**Langkah:**
1. Buka https://www.bps.go.id/
2. Menu **"Publikasi"** → **"Peta Tematik"**
3. Pilih: **Jawa Tengah** → **Kabupaten Cilacap**
4. Download shapefile kecamatan

### Opsi 4: Geoservices Indonesia (InaGeoportal)
**Website:** https://tanahair.indonesia.go.id/geoservices/

**Langkah:**
1. Buka https://tanahair.indonesia.go.id/geoservices/
2. **WFS Service** untuk administrative boundaries
3. Filter: `admin_level=4` (kecamatan)

## Setelah Download Shapefile

### 1. Extract ke folder data_raw
```bash
cd /home/timurlaut/semester7/metlit/OSMnx
mkdir -p data_raw/kecamatan_bps
unzip kecamatan_cilacap.zip -d data_raw/kecamatan_bps/
```

### 2. Buat script untuk load & process shapefile

File: `src/process_kecamatan_bps.py`

```python
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Path ke shapefile BPS
shp_path = 'data_raw/kecamatan_bps/kecamatan_cilacap.shp'

# Load shapefile
print(f"Loading shapefile: {shp_path}")
kecamatan_gdf = gpd.read_file(shp_path)

print(f"✓ Loaded {len(kecamatan_gdf)} kecamatan")
print(f"CRS: {kecamatan_gdf.crs}")

# Reproject ke EPSG:4326 jika perlu
if kecamatan_gdf.crs != 'EPSG:4326':
    kecamatan_gdf = kecamatan_gdf.to_crs('EPSG:4326')
    print("✓ Reprojected to EPSG:4326")

# Lihat kolom yang tersedia
print("\nKolom tersedia:", kecamatan_gdf.columns.tolist())

# Standardisasi nama kolom (sesuaikan dengan kolom di shapefile BPS)
# Biasanya: NAMOBJ, WADMKC, KDCPUM, dll
column_mapping = {
    'NAMOBJ': 'kecamatan',  # Nama kecamatan
    'WADMKC': 'kecamatan',  # Alternative
    'KDCPUM': 'kode',        # Kode kecamatan
}

for old_col, new_col in column_mapping.items():
    if old_col in kecamatan_gdf.columns:
        kecamatan_gdf.rename(columns={old_col: new_col}, inplace=True)
        break

kecamatan_gdf['kabupaten'] = 'Cilacap'
kecamatan_gdf['provinsi'] = 'Jawa Tengah'

# Sort by name
if 'kecamatan' in kecamatan_gdf.columns:
    kecamatan_gdf = kecamatan_gdf.sort_values('kecamatan')

print("\nKecamatan:")
for idx, row in kecamatan_gdf.iterrows():
    if 'kecamatan' in kecamatan_gdf.columns:
        print(f"  {idx+1}. {row['kecamatan']}")

# Save ke GeoJSON
output_dir = 'data_processed'
os.makedirs(output_dir, exist_ok=True)

geojson_path = f'{output_dir}/kecamatan_cilacap_bps.geojson'
kecamatan_gdf.to_file(geojson_path, driver='GeoJSON')
print(f"\n✅ Saved: {geojson_path}")

# Save ke shapefile
shp_output = f'{output_dir}/kecamatan_cilacap_bps.shp'
kecamatan_gdf.to_file(shp_output)
print(f"✅ Saved: {shp_output}")

# Visualisasi
fig, ax = plt.subplots(figsize=(14, 16))

kecamatan_gdf.plot(
    ax=ax,
    column='kecamatan' if 'kecamatan' in kecamatan_gdf.columns else None,
    cmap='tab20',
    edgecolor='black',
    linewidth=1.5,
    legend=False
)

# Add labels
if 'kecamatan' in kecamatan_gdf.columns:
    for idx, row in kecamatan_gdf.iterrows():
        centroid = row.geometry.centroid
        ax.text(
            centroid.x, centroid.y,
            row['kecamatan'],
            fontsize=8, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
        )

ax.set_title('Peta Kecamatan - Kabupaten Cilacap\n(Data BPS)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Latitude', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')

# North arrow
x, y = 0.95, 0.95
ax.annotate('N', xy=(x, y), xytext=(x, y-0.08),
            xycoords='axes fraction',
            fontsize=20, fontweight='bold',
            ha='center', va='center',
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))

plt.tight_layout()

vis_path = f'{output_dir}/kecamatan_map_bps.png'
plt.savefig(vis_path, dpi=300, bbox_inches='tight')
print(f"✅ Saved: {vis_path}")

plt.close()
```

### 3. Run script
```bash
python src/process_kecamatan_bps.py
```

## Alternatif: Manual Digitasi
Jika shapefile tidak tersedia, Anda bisa:
1. Download peta PDF dari BPS
2. Georeference di QGIS
3. Manual digitasi boundary
4. Export ke shapefile

## Kontak Support
- **BPS Cilacap:** https://cilacapkab.bps.go.id/
- **Portal Geospasial:** support@big.go.id
- **Hotline BPS:** 021-3841195

## Status Saat Ini
- ✅ **13 kecamatan** dari OSM (tersimpan di `kecamatan_cilacap.geojson`)
- ❌ **11 kecamatan** gagal: Cimanggu, Dayeuhluhur, Gandrungmangu, Jeruklegi, Kampung Laut, Kawunganten, Kedungreja, Kesugihan, Nusawungu, Patimuan, Wanareja
- 🎯 **Target:** 24 kecamatan lengkap dari shapefile BPS

## Rekomendasi
**Gunakan shapefile BPS** karena:
- ✅ Data resmi & akurat
- ✅ Lengkap semua 24 kecamatan
- ✅ Konsisten dengan statistik BPS
- ✅ Terupdate reguler
