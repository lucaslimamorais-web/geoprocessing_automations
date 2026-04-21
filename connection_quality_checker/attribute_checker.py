from qgis.core import *
from qgis.utils import iface
from collections import Counter

# Set your layer names here before running
layer_name_connections = "your_connection_layer"
layer_name_polygons = "your_polygon_layer"
layer_name_error = "ERROR"

# Choose your UTM zone: "22S" or "23S"
utm_zone = "23S"

# Map UTM zones to their EPSG codes
epsg_map = {
    "22S": 31982,
    "23S": 31983
}

if utm_zone not in epsg_map:
    raise Exception(f"Invalid UTM zone '{utm_zone}'. Use '22S' or '23S'.")

epsg_code = epsg_map[utm_zone]

# Grab the layers from the current project
layer_connections = QgsProject.instance().mapLayersByName(layer_name_connections)[0]
layer_polygons = QgsProject.instance().mapLayersByName(layer_name_polygons)[0]

# Make sure the user selected at least one polygon before running
selected = layer_polygons.selectedFeatures()
if not selected:
    raise Exception("No polygons selected. Please select at least one polygon and try again.")

# If the ERROR layer doesn't exist yet, create it as a temporary point layer
existing_error_layers = QgsProject.instance().mapLayersByName(layer_name_error)
if existing_error_layers:
    layer_error = existing_error_layers[0]
else:
    layer_error = QgsVectorLayer(f"Point?crs=EPSG:{epsg_code}", layer_name_error, "memory")
    provider = layer_error.dataProvider()
    provider.addAttributes([QgsField("INFO", QVariant.String)])
    layer_error.updateFields()
    QgsProject.instance().addMapLayer(layer_error)

# Points within this distance from the polygon border are considered connected
tolerance = 0.001

for polygon_feat in selected:
    polygon = polygon_feat.geometry()

    # Extract the polygon border to check which points are snapped to it
    if polygon.isMultipart():
        coords = polygon.asMultiPolygon()[0][0]
    else:
        coords = polygon.asPolygon()[0]

    border = QgsGeometry.fromPolylineXY(coords)

    # Collect attributes from all connection points snapped to this polygon
    point_attributes = []
    for connection in layer_connections.getFeatures():
        dist = connection.geometry().distance(border)
        if dist <= tolerance:
            attribute_1 = connection["ATTRIBUTE_1"]
            attribute_2 = connection["ATTRIBUTE_2"]
            attribute_3 = connection["ATTRIBUTE_3"]
            point_attributes.append((attribute_1, attribute_2, attribute_3))

    total = len(point_attributes)
    print(f"Polygon ID {polygon_feat.id()} — {total} connected point(s) found")

    if total > 0:
        count = Counter(point_attributes)
        most_common, freq = count.most_common(1)[0]
        ratio = freq / total

        print(f"Most common attributes: ATTRIBUTE_1={most_common[0]}, ATTRIBUTE_2={most_common[1]}, ATTRIBUTE_3={most_common[2]} ({freq}/{total})")

        # Flag discrepancy if 60%+ share the same attributes but not all do
        if ratio >= 0.6 and freq < total:
            print("⚠️ Discrepancy detected!")
            for attr, qty in count.items():
                if attr != most_common:
                    print(f"  - ATTRIBUTE_1={attr[0]}, ATTRIBUTE_2={attr[1]}, ATTRIBUTE_3={attr[2]} ({qty} point(s))")

            # Drop a point at the polygon center to mark it for review
            center = polygon.centroid().asPoint()
            error_feat = QgsFeature(layer_error.fields())
            error_feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(center)))
            error_feat.setAttribute("INFO", f"Discrepancy found in polygon ID {polygon_feat.id()}")
            layer_error.startEditing()
            layer_error.addFeature(error_feat)
            layer_error.commitChanges()
            print(f"✓ Error point added at polygon ID {polygon_feat.id()}")