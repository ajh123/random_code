from flask import Flask, jsonify, abort
from geojson2vt.geojson2vt import geojson2vt
import geojson
import json

app = Flask(__name__)

# Create GeoJSON FeatureCollection
point = geojson.Point((-3.68, 40.41))
feature = geojson.Feature(geometry=point, properties={"name": "Sample Point"})
feature_collection = geojson.FeatureCollection([feature])
geojson_data = geojson.dumps(feature_collection)

# Convert GeoJSON data to a Python dictionary
geojson_dict = json.loads(geojson_data)

# Create a tile index
tile_index = geojson2vt(geojson_dict, {})

@app.route('/tiles/<int:z>/<int:x>/<int:y>.json', methods=['GET'])
def get_tile(z, x, y):
    tile = tile_index.get_tile(z, x, y)
    if tile:
        return jsonify(tile)
    else:
        abort(404, description="Tile not found")

if __name__ == '__main__':
    app.run(debug=True)
