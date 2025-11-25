import osmnx as ox

# Set konfigurasi global OSMnx
ox.settings.log_console = True
ox.settings.use_cache = True

# 1. Tentukan wilayah
area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"

# 2. Ambil batas administrasi
boundary = ox.geocode_to_gdf(area)

print(boundary)
boundary.plot()
