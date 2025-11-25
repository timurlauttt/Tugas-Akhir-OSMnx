import os
import osmnx as ox
import matplotlib.pyplot as plt

ox.settings.log_console = True
ox.settings.use_cache = True

area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"
boundary = ox.geocode_to_gdf(area)

os.makedirs("data_processed", exist_ok=True)
boundary.to_file("data_processed/boundary.geojson", driver="GeoJSON")

print(boundary)
boundary.plot()
plt.show()