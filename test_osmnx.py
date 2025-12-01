import osmnx as ox

ox.settings.log_console = True
ox.settings.use_cache = True

area = "Kabupaten Cilacap, Jawa Tengah, Indonesia"

boundary = ox.geocode_to_gdf(area)

print(boundary)
boundary.plot()
