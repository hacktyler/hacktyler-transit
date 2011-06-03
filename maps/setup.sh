#!/bin/bash

createdb -T template_postgis transit

echo "INSERT into spatial_ref_sys (srid, auth_name, auth_srid, proj4text, srtext) values ( 900913, 'spatialreference.org', 6, '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs', 'PROJCS[\"unnamed\",GEOGCS[\"unnamed ellipse\",DATUM[\"unknown\",SPHEROID[\"unnamed\",6378137,0]],PRIMEM[\"Greenwich\",0]
,UNIT[\"degree\",0.0174532925199433]],PROJECTION[\"Mercator_2SP\"],PARAMETER[\"standard
_parallel_1\",0],PARAMETER[\"central_meridian\",0],PARAMETER[\"false_easting\",0],PARAMETER
[\"false_northing\",0],UNIT[\"Meter\",1],EXTENSION[\"PROJ4\",\"+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs\"]]');" | psql -q transit

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
