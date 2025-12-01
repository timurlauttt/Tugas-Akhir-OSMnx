import os
import glob
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

DATA_RAW = "data_raw"
OUTPUT_DIR = "data_processed"
os.makedirs(OUTPUT_DIR, exist_ok=True)

LAT_CAND = {"lat", "latitude", "y", "LAT", "Latitude", "Lat"}
LON_CAND = {"lon","lng","longitude","x","LON","Longitude","Lng","Long","LONG"}

def try_float(x):
    if pd.isna(x):
        return None
    if isinstance(x, str):
        x = x.strip().replace(",", ".")
    try:
        return float(x)
    except Exception:
        return None

def find_latlon_by_names(cols):
    lat = next((c for c in cols if str(c).strip() in LAT_CAND), None)
    lon = next((c for c in cols if str(c).strip() in LON_CAND), None)
    return lat, lon

def detect_latlon_by_values(df, sample_n=50):
    # evaluate each column for parseable numbers and whether they fit lat/lon ranges
    scores = {}
    nrows = min(len(df), sample_n)
    sample = df.head(nrows)
    for col in df.columns:
        vals = sample[col].apply(try_float)
        parsed = vals.notnull().sum()
        if parsed == 0:
            continue
        valsf = vals.dropna().astype(float)
        lat_in = ((valsf >= -90) & (valsf <= 90)).sum()
        lon_in = ((valsf >= -180) & (valsf <= 180)).sum()
        scores[col] = {
            "parsed_ratio": parsed / max(1, nrows),
            "lat_ratio": lat_in / parsed,
            "lon_ratio": lon_in / parsed
        }
    # choose best lat and lon candidates (must be different)
    lat_candidate = None
    lon_candidate = None
    best_lat_score = 0
    best_lon_score = 0
    for col, s in scores.items():
        lat_score = s["parsed_ratio"] * s["lat_ratio"]
        if lat_score > best_lat_score:
            best_lat_score = lat_score
            lat_candidate = col
        lon_score = s["parsed_ratio"] * s["lon_ratio"]
        if lon_score > best_lon_score:
            best_lon_score = lon_score
            lon_candidate = col
    # ensure distinct
    if lat_candidate == lon_candidate:
        # try second best for lon
        second_best = None
        second_score = 0
        for col, s in scores.items():
            if col == lat_candidate:
                continue
            lon_score = s["parsed_ratio"] * s["lon_ratio"]
            if lon_score > second_score:
                second_score = lon_score
                second_best = col
        lon_candidate = second_best
    return lat_candidate, lon_candidate

def header_looks_like_data(cols, threshold=2):
    # if several column names parse as numbers -> probably header row was actually data
    count = 0
    for c in cols:
        try:
            float(str(c))
            count += 1
        except Exception:
            continue
    return count >= threshold

# Hanya proses file Data_Desa_Rawan_Banjir_di_Cilacap.xlsx
flood_file = os.path.join(DATA_RAW, "Data_Desa_Rawan_Banjir_di_Cilacap.xlsx")
if not os.path.exists(flood_file):
    print(f"File tidak ditemukan: {flood_file}")
    exit(1)

path = flood_file
name = os.path.splitext(os.path.basename(path))[0]
print("PROCESS:", path)

# Baca Excel dengan header di baris pertama (row 0)
try:
    df = pd.read_excel(path, header=0)
    print("  columns:", list(df.columns)[:15])
except Exception as e:
    print("  failed to read:", e)
    exit(1)

# 1) try by column names (common headers)
lat_col, lon_col = find_latlon_by_names(df.columns)

# 2) if not found, try detect by values
if not lat_col or not lon_col:
    lat_col, lon_col = detect_latlon_by_values(df)
    if lat_col and lon_col:
        print(f"  detected lat/lon by values: lat='{lat_col}' lon='{lon_col}'")
    else:
        print(f"  NO lat/lon detected for {name}. Available columns: {list(df.columns)[:20]}")
        exit(1)

# ensure columns exist in df (if header=None columns are integers)
try:
    df[lat_col] = df[lat_col].apply(try_float)
    df[lon_col] = df[lon_col].apply(try_float)
except Exception:
    print("  failed applying clean on detected columns; exiting")
    exit(1)

# report invalid
invalid = df[df[[lat_col, lon_col]].isnull().any(axis=1)]
if not invalid.empty:
    inv_path = os.path.join(OUTPUT_DIR, f"{name}_invalid_coords.csv")
    invalid.to_csv(inv_path, index=False)
    print(f"  saved invalid rows to {inv_path} ({len(invalid)})")

# keep only valid rows
df_valid = df.dropna(subset=[lat_col, lon_col]).copy()
df_valid["__lat"] = df_valid[lat_col].astype(float)
df_valid["__lon"] = df_valid[lon_col].astype(float)

# validate ranges
mask = df_valid["__lat"].between(-90, 90) & df_valid["__lon"].between(-180, 180)
bad_range = df_valid[~mask]
if not bad_range.empty:
    br_path = os.path.join(OUTPUT_DIR, f"{name}_out_of_range.csv")
    bad_range.to_csv(br_path, index=False)
    print(f"  saved out-of-range rows to {br_path} ({len(bad_range)})")
df_valid = df_valid[mask]

# drop duplicates (exact coords)
df_valid = df_valid.drop_duplicates(subset=["__lat","__lon"])

# build GeoDataFrame and save
geometry = [Point(xy) for xy in zip(df_valid["__lon"], df_valid["__lat"])]
try:
    gdf = gpd.GeoDataFrame(df_valid.drop(columns=["__lat","__lon"]), geometry=geometry, crs="EPSG:4326")
except Exception:
    # fallback: keep only minimal columns if geopandas fails on dtype issues
    gdf = gpd.GeoDataFrame(df_valid.loc[:, []], geometry=geometry, crs="EPSG:4326")
out_path = os.path.join(OUTPUT_DIR, f"{name}.geojson")
gdf.to_file(out_path, driver="GeoJSON")
print("  saved:", out_path, "features:", len(gdf))