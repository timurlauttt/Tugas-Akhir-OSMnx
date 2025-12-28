# Tugas Akhir - OSMnx Mapping Project

Proyek pemetaan Kabupaten Cilacap menggunakan OSMnx untuk analisis spasial boundary, jalan, bangunan, titik rawan banjir, dan titik evakuasi.

---

##  Progress Tracking

###  Completed Tasks

#### 1. Setup Project Structure
- [x] Inisialisasi repository Git
- [x] Setup `.gitignore` untuk exclude folder data besar
- [x] Struktur folder: `src/`, `data_raw/`, `data_processed/`, `cache/`

#### 2. Data Acquisition & Processing
- [x] **Boundary Layer** (`get_boundary.py`)
  - Ambil boundary Kabupaten Cilacap dari OSM
  - Export ke `boundary.geojson` (1 polygon)
  - Visualisasi dengan warna hitam (#000000)
  
- [x] **Building Layer** (`get_building.py`)
  - Ambil data bangunan dari OSM (~953K features)
  - Export ke `building.geojson`
  - Visualisasi dengan warna orange/vermillion (#D55E00)
  
- [x] **Road Network** (`get_road.py`)
  - Ambil jaringan jalan dari OSM
  - Export ke `road.graphml` (network graph)
  - Visualisasi dengan warna biru (#0072B2)

#### 3. Visualization Improvements
- [x] Implementasi skema warna colorblind-friendly (Okabe-Ito palette)
- [x] Tambahkan legend pada setiap layer
- [x] Tambahkan petunjuk arah mata angin (North arrow)
- [x] Konsistensi styling antar semua file visualisasi

#### 4. Layered Visualization
- [x] `visualize_layer.py` - Overlay semua layer (boundary, roads, buildings)
- [x] Zorder management untuk layer visibility
- [x] Unified legend dengan semua layer

---

#### 5. Point Data Processing
- [x] **Flood Risk Points** (`get_floodpoint.py`)
  - Input: `data_raw/Data_Desa_Rawan_Banjir_di_Cilacap.xlsx` (130 rows)
  - Data cleaning: validasi koordinat, handling missing values
  - Auto-deteksi kolom latitude/longitude dengan fallback manual mapping
  - Export ke `Data_Desa_Rawan_Banjir_di_Cilacap.geojson` (127 valid features)
  - Report invalid: 3 baris tersimpan di `*_invalid_coords.csv`
  
- [x] **Evacuation Points** (`get_evac_point.py`)
  - Input: `data_raw/tempatevakuasinew.csv` (321 rows, tanpa header)
  - Data cleaning: normalisasi koordinat, manual mapping kolom 3 & 4
  - Export ke `tempatevakuasinew.geojson` (320 valid features)
#### 6. Individual Visualizations
- [x] **Boundary Visualization** (`visualize_boundary.py`)
  - Warna: Black (#000000)
  - Legend dan North arrow
  
- [x] **Flood Risk Visualization** (`visualize_flood.py`)
  - Warna: Green (#009E73) untuk flood-risk points
  - Marker: Circle (○)
  - Legend dan North arrow
  
- [x] **Evacuation Visualization** (`visualize_evac.py`)
  - Filter otomatis: deteksi evakuasi banjir/tsunami dari kolom `col_12`
  - Warna: Yellow (#F0E442) untuk evakuasi banjir/tsunami (△ besar)
  - Warna: Gray (#999999) untuk evakuasi bencana lain (△ kecil, transparan)
  - Legend dengan jumlah per kategori + summary stats
  - North arrow

#### 7. Integrated Visualization
- [x] **Layered Map** (`visualize_layer.py`)
  - Overlay **6 layers**: boundary, roads, buildings, flood points, evac (flood/tsunami), evac (other)
  - Zorder management untuk layer visibility optimal
  - Unified legend dengan semua layer dan jumlah features
  - Color scheme konsisten (colorblind-friendly)
  - North arrow di pojok kanan bawah

---

###  Todo / Planned Tasks

#### 8. Spatial Analysis (Optional Enhancement)

#### 7. Analysis & Documentation
- [ ] Spatial analysis: jarak titik evakuasi ke area rawan banjir
- [ ] Buffer analysis untuk coverage area evakuasi
- [ ] Network analysis: jalur evakuasi optimal
#### 8. Spatial Analysis (Optional Enhancement)
- [ ] Hitung jarak terdekat flood point → evacuation point
- [ ] Buffer analysis untuk coverage area evakuasi
- [ ] Network analysis: shortest path via road network
- [ ] Clustering titik rawan banjir per kecamatan
- [ ] Export hasil analisis ke CSV/Excel

#### 9. Interactive Visualization (Optional)
- [ ] Export ke Folium HTML map (interaktif)
- [ ] Web dashboard dengan Streamlit/Dash

#### 10. Quality Assurance
- [x] Validasi data koordinat (invalid rows tersimpan di CSV terpisah)
- [x] CRS consistency check (EPSG:4326)
- [ ] Verifikasi outlier koordinat
- [ ] Testing visualization di berbagai screen size
- [ ] Performance optimization untuk building layer (953K features)
- [ ] Validasi data koordinat untuk semua point layers
- [ ] Cek duplikasi data
- [ ] Verifikasi CRS consistency (EPSG:4326)
- [ ] Testing visualization di berbagai screen size

---

##  File Structure

```
OSMnx/
├── src/
│   ├── get_boundary.py          #  Ambil boundary Cilacap
│   ├── get_building.py          #  Ambil data bangunan
│   ├── get_road.py              #  Ambil jaringan jalan
│   ├── get_floodpoint.py        #  Convert XLSX → GeoJSON (flood points)
│   ├── get_evac_point.py        #  Convert CSV → GeoJSON (evac points)
│   ├── visualize_boundary.py    #  Visualisasi boundary
│   ├── visualize_building.py    #  Visualisasi buildings
│   ├── visualize_road.py        #  Visualisasi roads
│   ├── visualize_flood.py       #  Visualisasi flood-risk points
│   ├── visualize_evac.py        #  Visualisasi evacuation points
├── data_processed/               # Output GeoJSON/GraphML (ignored by git)
│   ├── boundary.geojson                                      # 1 polygon
│   ├── building.geojson                                      # ~953K features
│   ├── road.graphml                                          # network graph
│   ├── tempatevakuasinew.geojson                            # 320 features
│   ├── Data_Desa_Rawan_Banjir_di_Cilacap.geojson           # 127 features
│   ├── tempatevakuasinew_invalid_coords.csv                # 1 invalid row
│   └── Data_Desa_Rawan_Banjir_di_Cilacap_invalid_coords.csv # 3 invalid rows
├── data_processed/               # Output GeoJSON/GraphML (ignored by git)
│   ├── boundary.geojson
│   ├── building.geojson
│   ├── road.graphml
│   ├── tempatevakuasinew.geojson                  #  320 features
│   └── Data_Desa_Rawan_Banjir_di_Cilacap.geojson # 127 features
##  Color Scheme (Colorblind-Friendly)

| Layer | Color | Hex Code | Marker | Description |
|-------|-------|----------|--------|-------------|
| Boundary | Hitam / Black | `#000000` | Line | Batas administratif Kab. Cilacap |
| Roads | Biru / Blue | `#0072B2` | Line | Jaringan jalan (drive network) |
| Buildings | Orange | `#D55E00` | Polygon | Bangunan (~953K features) |
| Flood Risk | Hijau / Green | `#009E73` | ○ Circle | Titik rawan banjir (127 desa) |
| Evacuation (Flood/Tsunami) | Kuning / Yellow | `#F0E442` | △ Triangle (large) | Tempat evakuasi banjir/tsunami |
| Evacuation (Other) | Abu-abu / Gray | `#999999` | △ Triangle (small) | Tempat evakuasi bencana lain |
| Layer | Color | Hex Code | Marker |
|-------|-------|----------|--------|
| Boundary | Hitam / Black | `#000000` | Line |
| Roads | Biru / Blue | `#0072B2` | Line |
| Buildings | Orange | `#D55E00` | Polygon |
| Flood Risk | Hijau / Green | `#009E73` | ○ Circle |
| Evacuation (Flood/Tsunami) | Kuning / Yellow | `#F0E442` | △ Triangle |
| Evacuation (Other) | Abu-abu / Gray | `#999999` | △ Triangle |

---

##  How to Run

### Prerequisites
```bash
pip install osmnx geopandas matplotlib pandas shapely fiona pyproj openpyxl
```

### Generate Individual Layers
```bash
python src/get_boundary.py
python src/get_building.py
python src/get_road.py
```

### Process Point Data
```bash
python src/get_floodpoint.py
python src/get_evac_point.py
```

### Visualize Individual Layers
```bash
python src/visualize_flood.py
python src/visualize_evac.py
```

### Generate Combined Visualization
```bash
python src/visualize_layer.py
```

##  Data Sources & Statistics

### Input Data
- **Boundary, Roads, Buildings**: OpenStreetMap (via OSMnx API)
- **Flood Risk Points**: `Data_Desa_Rawan_Banjir_di_Cilacap.xlsx` 
  - Total: 130 rows → 127 valid features (3 invalid)
- **Evacuation Points**: `tempatevakuasinew.csv`
  - Total: 321 rows → 320 valid features (1 invalid)
##  Technical Notes

### Data Processing
- **CRS**: EPSG:4326 (WGS84) untuk semua layer
- **Coordinate Validation**: Otomatis validasi rentang lat/lon dan ekspor invalid rows ke CSV terpisah
- **Header Detection**: Auto-detect kolom latitude/longitude dengan fallback manual mapping (kolom 3 & 4)
- **Data Cleaning**: Normalisasi desimal (koma → titik), drop duplicates, drop NaN

### Visualization
- **Colorblind-Friendly**: Menggunakan palet Okabe-Ito (scientific standard)
- **Layer Order (zorder)**:
  1. Roads (zorder=2)
  2. Buildings (zorder=3)
##  Repository

**GitHub**: [timurlauttt/Tugas-Akhir-OSMnx](https://github.com/timurlauttt/Tugas-Akhir-OSMnx)

---

##  License

This project is for academic purposes (Tugas Akhir).

---

*Last Updated: December 13, 2025*  
*Project Status: 95% Complete (Core functionality done, spatial analysis optional)*
### Known Issues
- Building layer sangat besar (953 MB) → rendering bisa lambat
- 3 koordinat invalid di flood data (header rows)
- 1 koordinat invalid di evac data
- Folder `data_processed/`, `cache/`, dan `data/` tidak di-track oleh Git (file terlalu besar)
| `road.graphml` | Network | ~50 MB | Graph jaringan jalan |
| `Data_Desa_Rawan_Banjir_di_Cilacap.geojson` | 127 | ~30 KB | Titik rawan banjir |
| `tempatevakuasinew.geojson` | 320 | ~80 KB | Titik evakuasi |
- **Flood Risk Points**: `Data_Desa_Rawan_Banjir_di_Cilacap.xlsx` (127 desa rawan banjir)
- **Evacuation Points**: `tempatevakuasinew.csv` (320 lokasi evakuasi, termasuk banjir/tsunami dan bencana lain)

---

##  Notes

- Folder `data_processed/`, `cache/`, dan `data/` tidak di-track oleh Git (file terlalu besar)
- CRS: EPSG:4326 (WGS84) untuk semua layer
- Visualisasi menggunakan palet warna ramah buta warna (Okabe-Ito)
- North arrow ditampilkan di pojok kanan bawah setiap peta
- Auto-deteksi kolom latitude/longitude untuk file tanpa header yang konsisten
- Evakuasi banjir/tsunami diberi warna kuning (#F0E442), bencana lain abu-abu (#999999)

---

##  Repository

**GitHub**: [timurlauttt/Tugas-Akhir-OSMnx](https://github.com/timurlauttt/Tugas-Akhir-OSMnx)

---

*Last Updated: December 1, 2025*
