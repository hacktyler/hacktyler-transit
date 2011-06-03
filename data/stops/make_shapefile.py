#!/usr/bin/env python

import csv
import os
import shutil

from osgeo import ogr

try:
    shutil.rmtree('bus_stops_data')
except OSError:
    pass

os.mkdir('bus_stops_data')

shp_driver = ogr.GetDriverByName('ESRI Shapefile')
output = shp_driver.CreateDataSource("bus_stops_data/bus_stops_data.shp")

stops = output.CreateLayer("bus_stops_data", geom_type=ogr.wkbPoint)

fields = {
    'ORDER': ogr.OFTString,
    'LINE': ogr.OFTString,
    'DIRECTION': ogr.OFTString,
    'NAME': ogr.OFTString,
    'BLOCK': ogr.OFTString,
    'STREET': ogr.OFTString,
    'LANDMARK': ogr.OFTString,
    'MARKER': ogr.OFTString,
    'LATITUDE': ogr.OFTReal,
    'LONGITUDE': ogr.OFTReal,
    'TRANSFER': ogr.OFTString,
    'WEEKDAY': ogr.OFTString,
    'SATURDAY': ogr.OFTString,
    'OFC_TIMES': ogr.OFTString,
    'NOTES': ogr.OFTString,
}

for name, ogr_type in fields.items():
    field = ogr.FieldDefn(name, ogr_type)
    stops.CreateField(field)

with open('bus-stops-schedule.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        lat = row['latitude']
        lon = row['longitude']

        if not lat:
            continue

        feature = ogr.Feature(feature_def=stops.GetLayerDefn())

        feature.SetField('ORDER', row['order'])
        feature.SetField('LINE', row['line'])
        feature.SetField('DIRECTION', row['direction'])
        feature.SetField('NAME', row['name'])
        feature.SetField('BLOCK', row['block'])
        feature.SetField('STREET', row['street'])
        feature.SetField('LANDMARK', row['landmark'])
        feature.SetField('MARKER', row['marker'])
        feature.SetField('LATITUDE', row['latitude'])
        feature.SetField('LONGITUDE', row['longitude'])
        feature.SetField('TRANSFER', row['transfer_to'])
        feature.SetField('WEEKDAY', row['weekday_schedule'])
        feature.SetField('SATURDAY', row['saturday_schedule'])
        feature.SetField('OFC_TIMES', row['has_official_times'])
        feature.SetField('NOTES', row['notes'])

        wkt = "POINT(%s %s)" % (row['longitude'], row['latitude'])
        point = ogr.CreateGeometryFromWkt(wkt)

        feature.SetGeometryDirectly(point)
        stops.CreateFeature(feature)

        feature.Destroy()

output.Destroy()    
