#!/usr/bin/env python

from osgeo import ogr

ds = ogr.Open("bus_stops_4326/bus_stops_4326.shp")
layer = ds.GetLayerByName("bus_stops_4326")

layer.ResetReading()

points = []

for feature in layer:
    stop_id = feature.GetFieldAsInteger(5)
    geom = feature.GetGeometryRef()

    points.append((stop_id, geom.GetX(), geom.GetY()))

with open("pts.csv", "w") as f:
    for pt in points:
        f.write("%s,%s,%s\n" % pt)

ds = None
