# Vertex Connection Markers

Generates a point layer in ArcGIS Pro marking the first and last vertex of each feature in a line layer.

## Problem

When working with read-only layers alongside editable shapefiles, connecting new features to existing ones later becomes difficult without a clear reference of where the connections should be made.

## Solution

This script extracts the first and last vertex of each line feature and creates a point shapefile to serve as visual connection markers — making it easy to identify exactly where features need to be connected later.

## How to use

1. Open the script and set the following variables:
   - `workspace`: path to your working folder
   - `input_layer`: name of your line layer in ArcGIS Pro
2. Run the script in ArcGIS Pro
3. A new point layer called `Referencia_Interligacao.shp` will be created in your workspace

## Requirements

- ArcGIS Pro with a valid license
- Python environment provided by ArcGIS Pro (arcpy)