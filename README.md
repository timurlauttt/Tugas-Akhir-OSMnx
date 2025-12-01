# Tugas Akhir - OSMnx Mapping Project

Proyek pemetaan Kabupaten Cilacap menggunakan OSMnx untuk analisis spasial boundary, jalan, bangunan, titik rawan banjir, dan titik evakuasi.

---

## 📋 Progress Tracking

### ✅ Completed Tasks

#### 1. Setup Project Structure
- [x] Inisialisasi repository Git
- [x] Setup `.gitignore` untuk exclude folder data besar
- [x] Struktur folder: `src/`, `data_raw/`, `data_processed/`, `cache/`

#### 2. Data Acquisition & Processing
- [x] **Boundary Layer** (`get_boundary.py`)
  - Ambil boundary Kabupaten Cilacap dari OSM
  - Export ke `boundary.geojson`
  - Visualisasi dengan warna hitam (#000000)
  
- [x] **Building Layer** (`get_building.py`)
  - Ambil data bangunan dari OSM
  - Export ke `building.geojson`
  - Visualisasi dengan warna orange/vermillion (#D55E00)
  
- [x] **Road Network** (`get_road.py`)
  - Ambil jaringan jalan dari OSM
  - Export ke `road.graphml`
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
  - Input: `data_raw/Data_Desa_Rawan_Banjir_di_Cilacap.xlsx`
  - Data cleaning: validasi koordinat, handling missing values
  - Auto-deteksi kolom latitude/longitude
  - Export ke `Data_Desa_Rawan_Banjir_di_Cilacap.geojson` (127 features)
  
- [x] **Evacuation Points** (`get_evac_point.py`)
  - Input: `data_raw/tempatevakuasinew.csv`
  - Data cleaning: normalisasi koordinat, manual mapping kolom
  - Export ke `tempatevakuasinew.geojson` (320 features)

#### 6. Individual Visualizations
- [x] **Flood Risk Visualization** (`visualize_flood.py`)
  - Warna: Green (#009E73) untuk flood-risk points
  - Marker: Circle (○)
  - Legend dan North arrow
  
- [x] **Evacuation Visualization** (`visualize_evac.py`)
  - Warna: Yellow (#F0E442) untuk evakuasi banjir/tsunami
  - Warna: Gray (#999999) untuk evakuasi bencana lain
  - Marker: Triangle (△)
  - Legend dengan jumlah per kategori

---

### 🔄 In Progress

#### 7. Integration & Final Visualization
- [ ] Integrate flood points ke `visualize_layer.py`
- [ ] Integrate evacuation points ke `visualize_layer.py`
- [ ] Overlay semua layer (boundary, roads, buildings, flood, evacuation)

---

### 📝 Todo / Planned Tasks

#### 7. Analysis & Documentation
- [ ] Spatial analysis: jarak titik evakuasi ke area rawan banjir
- [ ] Buffer analysis untuk coverage area evakuasi
- [ ] Network analysis: jalur evakuasi optimal
- [ ] Export hasil analisis ke format laporan

#### 8. Quality Assurance

#### 7. Analysis & Documentation
- [ ] Spatial analysis: jarak titik evakuasi ke area rawan banjir
- [ ] Buffer analysis untuk coverage area evakuasi
- [ ] Network analysis: jalur evakuasi optimal
- [ ] Export hasil analisis ke format laporan

#### 8. Quality Assurance
- [ ] Validasi data koordinat untuk semua point layers
- [ ] Cek duplikasi data
- [ ] Verifikasi CRS consistency (EPSG:4326)
- [ ] Testing visualization di berbagai screen size

---

## 🗂️ File Structure

```
OSMnx/
├── src/
│   ├── get_boundary.py          # ✅ Ambil boundary Cilacap
│   ├── get_building.py          # ✅ Ambil data bangunan
│   ├── get_road.py              # ✅ Ambil jaringan jalan
│   ├── get_floodpoint.py        # ✅ Convert XLSX → GeoJSON (flood points)
│   ├── get_evac_point.py        # ✅ Convert CSV → GeoJSON (evac points)
│   ├── visualize_boundary.py    # ✅ Visualisasi boundary
│   ├── visualize_building.py    # ✅ Visualisasi buildings
│   ├── visualize_road.py        # ✅ Visualisasi roads
│   ├── visualize_flood.py       # ✅ Visualisasi flood-risk points
│   ├── visualize_evac.py        # ✅ Visualisasi evacuation points
│   └── visualize_layer.py       # ✅ Overlay boundary + roads + buildings
│
├── data_raw/
│   ├── tempatevakuasinew.csv                       # Input: titik evakuasi
│   └── Data_Desa_Rawan_Banjir_di_Cilacap.xlsx     # Input: titik rawan banjir
│
├── data_processed/               # Output GeoJSON/GraphML (ignored by git)
│   ├── boundary.geojson
│   ├── building.geojson
│   ├── road.graphml
│   ├── tempatevakuasinew.geojson                  # ✅ 320 features
│   └── Data_Desa_Rawan_Banjir_di_Cilacap.geojson # ✅ 127 features
│
├── cache/                        # OSMnx cache (ignored by git)
├── .gitignore
└── README.md
```

---

## 🎨 Color Scheme (Colorblind-Friendly)

| Layer | Color | Hex Code | Marker |
|-------|-------|----------|--------|
| Boundary | Hitam / Black | `#000000` | Line |
| Roads | Biru / Blue | `#0072B2` | Line |
| Buildings | Orange | `#D55E00` | Polygon |
| Flood Risk | Hijau / Green | `#009E73` | ○ Circle |
| Evacuation (Flood/Tsunami) | Kuning / Yellow | `#F0E442` | △ Triangle |
| Evacuation (Other) | Abu-abu / Gray | `#999999` | △ Triangle |

---

## 🚀 How to Run

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

---

## 📊 Data Sources

- **Boundary, Roads, Buildings**: OpenStreetMap (via OSMnx)
- **Flood Risk Points**: `Data_Desa_Rawan_Banjir_di_Cilacap.xlsx` (127 desa rawan banjir)
- **Evacuation Points**: `tempatevakuasinew.csv` (320 lokasi evakuasi, termasuk banjir/tsunami dan bencana lain)

---

## 📌 Notes

- Folder `data_processed/`, `cache/`, dan `data/` tidak di-track oleh Git (file terlalu besar)
- CRS: EPSG:4326 (WGS84) untuk semua layer
- Visualisasi menggunakan palet warna ramah buta warna (Okabe-Ito)
- North arrow ditampilkan di pojok kanan bawah setiap peta
- Auto-deteksi kolom latitude/longitude untuk file tanpa header yang konsisten
- Evakuasi banjir/tsunami diberi warna kuning (#F0E442), bencana lain abu-abu (#999999)

---

## 🔗 Repository

**GitHub**: [timurlauttt/Tugas-Akhir-OSMnx](https://github.com/timurlauttt/Tugas-Akhir-OSMnx)

---

*Last Updated: December 1, 2025*
