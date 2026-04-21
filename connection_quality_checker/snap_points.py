from qgis.core import *
from qgis.utils import iface
import math

# Set your layer names here before running
layer_name_points = "your_point_layer"
layer_name_polygons = "your_polygon_layer"

def extract_border(geom):
    # Fix any invalid geometry before trying to extract the border
    if not geom.isGeosValid():
        geom = geom.makeValid()
    border = geom.convertToType(QgsWkbTypes.LineGeometry, destMultipart=True)
    if border is not None and not border.isEmpty():
        return border
    return None

def is_valid_geometry(geom):
    # Skip geometries that are null, empty or have an unknown type
    if geom is None:
        return False
    if geom.isEmpty():
        return False
    if geom.wkbType() == QgsWkbTypes.Unknown:
        return False
    return True

# Grab the layers from the current project
layers_points = QgsProject.instance().mapLayersByName(layer_name_points)
layers_polygons = QgsProject.instance().mapLayersByName(layer_name_polygons)

if not layers_points:
    raise Exception(f"Point layer '{layer_name_points}' not found. Check the layer name and try again.")
if not layers_polygons:
    raise Exception(f"Polygon layer '{layer_name_polygons}' not found. Check the layer name and try again.")

layer_points = layers_points[0]
layer_polygons = layers_polygons[0]

# Make sure the user selected at least one point before running
selected_points = layer_points.selectedFeatures()
if not selected_points:
    raise Exception("No points selected. Please select at least one point and try again.")

points_to_process = selected_points

if not layer_points.isEditable():
    layer_points.startEditing()

points_moved = 0

for point_feat in points_to_process:
    point_geom = point_feat.geometry()

    # Find the closest polygon to this point
    min_distance = float('inf')
    closest_polygon = None

    for polygon_feat in layer_polygons.getFeatures():
        polygon_geom = polygon_feat.geometry()
        if not is_valid_geometry(polygon_geom):
            continue
        distance = point_geom.distance(polygon_geom)
        if distance < 0:
            distance = 0
        if distance < min_distance:
            min_distance = distance
            closest_polygon = polygon_geom

    if not closest_polygon:
        continue

    # Extract the border and snap the point to the nearest spot on it
    border = extract_border(closest_polygon)
    if border is None or border.isEmpty():
        continue

    snapped_point = border.nearestPoint(point_geom).asPoint()
    new_geometry = QgsGeometry.fromPointXY(snapped_point)

    success = layer_points.changeGeometry(point_feat.id(), new_geometry)
    if success:
        points_moved += 1

# Save all changes
if layer_points.commitChanges():
    print(f"Done! {points_moved} point(s) successfully snapped to polygon borders.")
else:
    print("Something went wrong while saving. Rolling back changes.")
    layer_points.rollBack()

# Refresh the map canvas to show the updated positions
layer_points.triggerRepaint()
iface.mapCanvas().refresh()
print("Process complete.")