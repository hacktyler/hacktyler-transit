#!/bin/bash

# Run the entire process to update the stop data
cd data/stops
./compute_estimated_schedule.py
./make_json.py
./make_shapefile.py

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" bus_stops_data/bus_stops_data.shp -nln bus_stops -t_srs EPSG:900913 -overwrite

cd ../../maps
./make_xml.sh
./make_maps.py
