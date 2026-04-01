import arcpy
import os

# ⚠️ Set the path to your working folder
workspace = r"C:\path\to\your\folder"
arcpy.env.workspace = workspace

# ⚠️ Name of your line layer in ArcGIS Pro
input_layer = "your_layer_name"

# Output
output = os.path.join(workspace, "connection_markers.shp")

# Creates the point shapefile if it doesn't exist
if not arcpy.Exists(output):
    arcpy.CreateFeatureclass_management(workspace, "connection_markers.shp", "POINT")

# Iterates through features and inserts reference points at each vertex
with arcpy.da.SearchCursor(input_layer, ["SHAPE@"]) as cursor_in, \
     arcpy.da.InsertCursor(output, ["SHAPE@"]) as cursor_out:
    
    for row in cursor_in:
        line = row[0]
        first_vertex = arcpy.PointGeometry(line.firstPoint, line.spatialReference)
        last_vertex = arcpy.PointGeometry(line.lastPoint, line.spatialReference)
        cursor_out.insertRow([first_vertex])
        cursor_out.insertRow([last_vertex])

print("Reference points added at all feature vertices.")