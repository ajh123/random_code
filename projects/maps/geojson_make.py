from shapely.geometry import Point, LineString, Polygon
import geojson

# Create geometries with shapely
point = Point(102.0, 0.5)
line = LineString([(102.0, 0.0), (103.0, 1.0), (104.0, 0.0), (105.0, 1.0)])
polygon = Polygon([(100.0, 0.0), (101.0, 0.0), (101.0, 1.0), (100.0, 1.0)])

# Create features from shapely geometries
features = [
    geojson.Feature(geometry=geojson.loads(geojson.dumps(point.__geo_interface__)), properties={"name": "Point"}),
    geojson.Feature(geometry=geojson.loads(geojson.dumps(line.__geo_interface__)), properties={"name": "Line"}),
    geojson.Feature(geometry=geojson.loads(geojson.dumps(polygon.__geo_interface__)), properties={"name": "Polygon"})
]

# Feature collection and export to file
feature_collection = geojson.FeatureCollection(features)
with open("custom_data.geojson", "w") as f:
    geojson.dump(feature_collection, f)
