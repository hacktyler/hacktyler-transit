#!/bin/bash

wget http://downloads.cloudmade.com/americas/northern_america/united_states/texas/texas.osm.bz2
bunzip2 texas.osm.bz2
osm2pgsql --bbox -95.393,32.2307,-95.1933,32.4309 --database transit --create texas.osm

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" ../data/stops/bus_stops_data/bus_stops_data.shp -nln bus_stops -t_srs EPSG:900913

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" ../data/routes/bus_routes_4326/bus_routes_4326.shp -nln bus_routes -t_srs EPSG:900913

echo "ALTER TABLE bus_routes RENAME COLUMN ROUTE TO line" | psql -q transit

wget http://www.smithcountymapsite.org/webshare/downloads/railroads.zip
unzip railroads.zip

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" Railroads.shp -nln railroads -t_srs EPSG:900913

wget http://www.smithcountymapsite.org/webshare/downloads/parks.zip
unzip parks.zip

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" Parks.shp -nln parks -t_srs EPSG:900913 -nlt multipolygon

wget http://www.smithcountymapsite.org/webshare/downloads/structures.zip
unzip structures.zip

ogr2ogr -f "PostgreSQL" PG:"dbname=transit" Structures.shp -nln buildings -t_srs EPSG:900913
