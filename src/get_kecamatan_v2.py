"""
Mengambil boundary kecamatan di Kabupaten Cilacap menggunakan admin_level tag
Alternative approach yang lebih reliable dari geocoding by name
"""

import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import os

# Setup output directory
os.makedirs('data_processed', exist_ok=True)

print("Mengambil semua kecamatan (admin_level=7) di Kabupaten Cilacap...")

try:
    # Query semua administrative boundaries level 7 (kecamatan) dalam Kabupaten Cilacap
    # admin_level=7 adalah level kecamatan di Indonesia
    kecamatan_gdf = ox.features_from_place(
        "Kabupaten Cilacap, Jawa Tengah, Indonesia",
        tags={
            "admin_level": "7",  # Level kecamatan
            "boundary": "administrative"
        }
    )
    
    print(f"✓ Berhasil mengambil {len(kecamatan_gdf)} kecamatan")
    
    # Filter hanya geometry Polygon/MultiPolygon
    kecamatan_gdf = kecamatan_gdf[kecamatan_gdf.geometry.type.isin(['Polygon', 'MultiPolygon'])]
    print(f"  Setelah filter geometry: {len(kecamatan_gdf)} kecamatan")
    
    # Filter: hanya yang punya 'name' dan exclude dusun/RW/kantor
    if 'name' in kecamatan_gdf.columns:
        kecamatan_gdf = kecamatan_gdf[kecamatan_gdf['name'].notna()].copy()
        
        # Exclude: RW, Dusun, Desa, Kelurahan, Kantor, Balai, dll
        exclude_patterns = [
            'RW ', 'Dusun ', 'Desa ', 'Kelurahan ', 'Kantor ', 'Balai ',
            'Lakbok', 'Langensari', 'Mekarharja', 'Pataruman', 'Purwadadi',
            'Purwaharja', 'Rejasari', 'Sinartanjung', 'Waringinsari', 'Cintaratu',
            'Banjar', 'Jawa Barat', 'Jawa Tengah', 'Banyumas', 'Brebes', 'Ciamis',
            'Kebumen', 'Kuningan', 'Pangandaran'
        ]
        
        for pattern in exclude_patterns:
            kecamatan_gdf = kecamatan_gdf[~kecamatan_gdf['name'].str.contains(pattern, case=False, na=False)]
        
        print(f"  Setelah filter subdivisi: {len(kecamatan_gdf)} kecamatan")
    
    # Ambil kolom penting
    columns_to_keep = ['name', 'admin_level', 'boundary', 'geometry']
    available_columns = [col for col in columns_to_keep if col in kecamatan_gdf.columns]
    kecamatan_gdf = kecamatan_gdf[available_columns].copy()
    
    # Rename untuk konsistensi
    if 'name' in kecamatan_gdf.columns:
        kecamatan_gdf['kecamatan'] = kecamatan_gdf['name']
    
    kecamatan_gdf['kabupaten'] = 'Cilacap'
    kecamatan_gdf['provinsi'] = 'Jawa Tengah'
    
    # Sort by name
    if 'kecamatan' in kecamatan_gdf.columns:
        kecamatan_gdf = kecamatan_gdf.sort_values('kecamatan').reset_index(drop=True)
    
    print("\nKecamatan yang ditemukan:")
    if 'kecamatan' in kecamatan_gdf.columns:
        for idx, name in enumerate(kecamatan_gdf['kecamatan'], 1):
            print(f"  {idx}. {name}")
    
    # Save ke GeoJSON
    geojson_path = 'data_processed/kecamatan_cilacap_v2.geojson'
    kecamatan_gdf.to_file(geojson_path, driver='GeoJSON')
    print(f"\n✅ Saved: {geojson_path}")
    print(f"   Total kecamatan: {len(kecamatan_gdf)}")
    
    # Save ke Shapefile
    shp_path = 'data_processed/kecamatan_cilacap_v2.shp'
    kecamatan_gdf.to_file(shp_path)
    print(f"✅ Saved: {shp_path}")
    
    # Visualisasi
    print("\n🎨 Generating visualization...")
    fig, ax = plt.subplots(figsize=(14, 16))
    
    # Plot dengan warna berbeda tiap kecamatan
    kecamatan_gdf.plot(
        ax=ax,
        column='kecamatan' if 'kecamatan' in kecamatan_gdf.columns else None,
        cmap='tab20',
        edgecolor='black',
        linewidth=1.5,
        legend=False
    )
    
    # Add labels di centroid
    if 'kecamatan' in kecamatan_gdf.columns:
        for idx, row in kecamatan_gdf.iterrows():
            centroid = row.geometry.centroid
            ax.text(
                centroid.x, 
                centroid.y, 
                row['kecamatan'],
                fontsize=8,
                ha='center',
                va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7)
            )
    
    # Styling
    ax.set_title('Peta Kecamatan - Kabupaten Cilacap\n(OSM admin_level=7)', 
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
    
    # Save visualization
    vis_path = 'data_processed/kecamatan_map_v2.png'
    plt.savefig(vis_path, dpi=300, bbox_inches='tight')
    print(f"✅ Saved visualization: {vis_path}")
    
    plt.close()

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nAlternative: Gunakan shapefile dari BPS/Geospasial Indonesia")
