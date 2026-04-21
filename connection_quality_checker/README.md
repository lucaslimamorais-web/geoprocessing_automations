# Connection Quality Checker

A two-step workflow for snapping point features to polygon borders and validating their attributes in QGIS.

## The Problem

When working with point and polygon layers, points may not be precisely snapped to the polygon borders they belong to, and their attributes may not match the polygon they are associated with. Identifying and fixing these issues manually is time-consuming, especially at scale.

## The Solution

Two scripts that work together to ensure geometric and attribute consistency between point and polygon layers.

## Workflow

### Step 1 — Snap Points to Polygon Borders (`snap_points.py`)

Moves each selected point to the nearest segment of the closest polygon border. This ensures all points are geometrically connected to their corresponding polygons.

**How to use:**
1. Set `layer_name_points` and `layer_name_polygons` with your layer names
2. Select the points you want to snap
3. Run the script in QGIS

### Step 2 — Validate Attributes (`attribute_checker.py`)

Compares the attributes of the snapped points against the polygon they belong to. If a discrepancy is detected, a point is added to the center of that polygon in a temporary layer called `ERROR` for easy identification.

**How to use:**
1. Set `layer_name_connections`, `layer_name_polygons` and `utm_zone` with your values
2. Replace `ATTRIBUTE_1`, `ATTRIBUTE_2` and `ATTRIBUTE_3` with your actual attribute field names
3. Select the polygons you want to validate
4. Run the script in QGIS

## Requirements

- QGIS 3.x or higher
- Both scripts must be run inside the QGIS Python Console