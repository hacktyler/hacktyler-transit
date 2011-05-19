import csv
import os
import shutil

from osgeo import ogr

shutil.rmtree('bus-stops')
os.mkdir('bus-stops')

shp_driver = ogr.GetDriverByName('ESRI Shapefile')
output = shp_driver.CreateDataSource("bus-stops/bus-stops.shp")

stops = output.CreateLayer("bus-stops", geom_type=ogr.wkbPoint)

fields = {
    'LINE': ogr.OFTString,
    'ORDER': ogr.OFTString,
    'STOP_ST': ogr.OFTString,
    'CROSS_ST': ogr.OFTString,
    'LANDMARK': ogr.OFTString,
    'SHELTER': ogr.OFTString,
    'SIGN': ogr.OFTString,
    'FLAG': ogr.OFTString
}

for name, ogr_type in fields.items():
    field = ogr.FieldDefn(name, ogr_type)
    stops.CreateField(field)

with open('bus-stops.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        lat = row['latitude']
        lon = row['longitude']

        if not lat:
            continue

        feature = ogr.Feature(feature_def=stops.GetLayerDefn())

        feature.SetField('LINE', row['line'])
        feature.SetField('ORDER', row['order'])
        feature.SetField('STOP_ST', row['stop_street'])
        feature.SetField('CROSS_ST', row['next_cross_street'])
        feature.SetField('LANDMARK', row['landmark'])
        feature.SetField('SHELTER', row['shelter'])
        feature.SetField('SIGN', row['sign'])
        feature.SetField('FLAG', row['flag'])

        wkt = "POINT(%s %s)" % (row['longitude'], row['latitude'])
        point = ogr.CreateGeometryFromWkt(wkt)

        feature.SetGeometryDirectly(point)
        stops.CreateFeature(feature)

        feature.Destroy()

output.Destroy()    
