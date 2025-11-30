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

### 🔄 In Progress

#### 5. Point Data Processing
- [ ] **Flood Risk Points** (`get_floodpoint.py`)
  - Input: `data_raw/Data Desa Rawan Banjir di Cilacap.xlsx`
  - Data cleaning: validasi koordinat, handling missing values
  - Export ke `flood_points.geojson`
  
- [ ] **Evacuation Points** (`get_evac_point.py`)
  - Input: `data_raw/tempatevakuasinew.csv`
  - Data cleaning: normalisasi koordinat (koma → titik)
  - Export ke `evac_points.geojson`

---

### 📝 Todo / Planned Tasks

#### 6. Integration & Final Visualization
- [ ] Integrate flood points ke `visualize_layer.py`
  - Warna: Green (#009E73)
  - Marker: Circle (○)
  
- [ ] Integrate evacuation points ke `visualize_layer.py`
  - Warna: Yellow (#F0E442)
  - Marker: Triangle (△)

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
│   ├── get_evac_point.py        # 🔄 Convert CSV → GeoJSON
│   ├── get_floodpoint.py        # 🔄 Convert XLSX → GeoJSON
│   └── visualize_layer.py       # ✅ Overlay semua layer
│
├── data_raw/
│   ├── tempatevakuasinew.csv               # Input: titik evakuasi
│   └── Data Desa Rawan Banjir di Cilacap.xlsx  # Input: titik rawan banjir
│
├── data_processed/               # Output GeoJSON/GraphML (ignored by git)
│   ├── boundary.geojson
│   ├── building.geojson
│   ├── road.graphml
│   ├── evac_points.geojson      # TODO
│   └── flood_points.geojson     # TODO
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
| Evacuation | Kuning / Yellow | `#F0E442` | △ Triangle |

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

### Process Point Data (TODO)
```bash
python src/get_evac_point.py
python src/get_floodpoint.py
```

### Generate Combined Visualization
```bash
python src/visualize_layer.py
```

---

## 📊 Data Sources

- **Boundary, Roads, Buildings**: OpenStreetMap (via OSMnx)
- **Flood Risk Points**: `Data Desa Rawan Banjir di Cilacap.xlsx`
- **Evacuation Points**: `tempatevakuasinew.csv`

---

## 📌 Notes

- Folder `data_processed/`, `cache/`, dan `data/` tidak di-track oleh Git (file terlalu besar)
- CRS: EPSG:4326 (WGS84) untuk semua layer
- Visualisasi menggunakan palet warna ramah buta warna (Okabe-Ito)
- North arrow ditampilkan di pojok kanan bawah setiap peta

---

## 🔗 Repository

**GitHub**: [timurlauttt/Tugas-Akhir-OSMnx](https://github.com/timurlauttt/Tugas-Akhir-OSMnx)

---

*Last Updated: November 30, 2025*
