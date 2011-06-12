#!/usr/bin/python

# Inspired by generate_tiles.py, part of the Open Street Map project:
# http://svn.openstreetmap.org/applications/rendering/mapnik/generate_tiles.py

import argparse
from math import pi, sin, log, exp, atan
import multiprocessing
import Queue
import os

import mapnik2

mapnik2.register_fonts('/Library/Fonts/')
mapnik2.register_fonts('/usr/share/fonts')

DEFAULT_TILE_WIDTH = 256
DEFAULT_TILE_HEIGHT = 256
DEFAULT_MIN_ZOOM = 9
DEFAULT_MAX_ZOOM = 12
DEFAULT_PROCESS_COUNT = 2
DEFAULT_FILE_TYPE = 'png256'

DEG_TO_RAD = pi / 180
RAD_TO_DEG = 180 / pi

def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a

class GoogleProjection:
    """
    Google projection transformations. Sourced from the OSM.
    Have not taken the time to figure out how this works.
    """
    def __init__(self, levels=18):
        self.Bc = []
        self.Cc = []
        self.zc = []
        self.Ac = []
        c = 256

        for d in range(levels + 1):
            e = c/2;
            self.Bc.append(c/360.0)
            self.Cc.append(c/(2 * pi))
            self.zc.append((e,e))
            self.Ac.append(c)
            c *= 2
                
    def fromLLtoPixel(self, ll, zoom):
         d = self.zc[zoom]
         e = round(d[0] + ll[0] * self.Bc[zoom])
         f = minmax(sin(DEG_TO_RAD * ll[1]),-0.9999,0.9999)
         g = round(d[1] + 0.5*log((1+f)/(1-f))*-self.Cc[zoom])
         return (e,g)
     
    def fromPixelToLL(self, px, zoom):
         e = self.zc[zoom]
         f = (px[0] - e[0])/self.Bc[zoom]
         g = (px[1] - e[1])/-self.Cc[zoom]
         h = RAD_TO_DEG * ( 2 * atan(exp(g)) - 0.5 * pi)
         return (f,h)

class Renderer(multiprocessing.Process):
    """
    A tile renderer optimized for running in an isolated process.
    """
    def __init__(self, tile_queue, config, width=DEFAULT_TILE_WIDTH, height=DEFAULT_TILE_HEIGHT, filetype=DEFAULT_FILE_TYPE):
        multiprocessing.Process.__init__(self)

        self.killed = False

        self.config = config
        self.tile_queue = tile_queue
        self.width = width
        self.height = height
        self.filetype = filetype

    def run(self):
        self.mapnik_map = mapnik2.Map(self.width, self.height)
        mapnik2.load_map(self.mapnik_map, self.config, True)
        self.map_projection = mapnik2.Projection(self.mapnik_map.srs)

        self.tile_projection = GoogleProjection()  

        while not self.killed:
            try:
                tile_parameters = self.tile_queue.get_nowait()
            except Queue.Empty:
                break

            self.render_tile(*tile_parameters)
            self.tile_queue.task_done()

    def render_tile(self, filename, x, y, zoom):
        print 'Rendering %s' % (filename)

        # Calculate pixel positions of bottom-left & top-right
        half_width = self.width / 2
        half_height = self.height / 2
        p0 = (x * self.width, (y + 1) * self.height)
        p1 = ((x + 1) * self.width, y * self.height)

        # Convert tile coords to LatLng
        l0 = self.tile_projection.fromPixelToLL(p0, zoom);
        l1 = self.tile_projection.fromPixelToLL(p1, zoom);
        
        # Convert LatLng to map coords
        c0 = self.map_projection.forward(mapnik2.Coord(l0[0], l0[1]))
        c1 = self.map_projection.forward(mapnik2.Coord(l1[0], l1[1]))

        # Create bounding box for the render
        bbox = mapnik2.Box2d(c0.x, c0.y, c1.x, c1.y)

        self.mapnik_map.zoom_to_box(bbox)
        self.mapnik_map.buffer_size = max([half_width, half_height]) 

        # Render image with default Agg renderer
        image = mapnik2.Image(self.width, self.height)
        mapnik2.render(self.mapnik_map, image)
        image.save(filename, self.filetype)

def render_tiles(bbox, config, tile_dir, min_zoom=DEFAULT_MIN_ZOOM, max_zoom=DEFAULT_MAX_ZOOM, process_count=DEFAULT_PROCESS_COUNT):
    """
    Renders a batch of tiles for a given bounding-box.
    """
    if not os.path.isdir(tile_dir):
         os.mkdir(tile_dir)

    tile_projection = GoogleProjection(max_zoom) 

    ll0 = (bbox[1], bbox[0])
    ll1 = (bbox[3], bbox[2])

    tile_queue = multiprocessing.JoinableQueue()

    for z in range(min_zoom, max_zoom + 1):
        px0 = tile_projection.fromLLtoPixel(ll0, z)
        px1 = tile_projection.fromLLtoPixel(ll1, z)

        tile_x1 = int(px0[0] / 256.0)
        tile_x2 = int(px1[0] / 256.0) + 1
        tile_y1 = int(px0[1] / 256.0)
        tile_y2 = int(px1[1] / 256.0) + 1

        zoom_dir = os.path.join(tile_dir, str(z))

        if not os.path.isdir(zoom_dir):
            os.mkdir(zoom_dir)

        for x in range(tile_x1, tile_x2):
            # Validate x coordinate
            if (x < 0) or (x >= 2**z):
                continue

            x_dir = os.path.join(zoom_dir, str(x))

            if not os.path.isdir(x_dir):
                os.mkdir(x_dir)

            for y in range(tile_y1, tile_y2):
                # Validate y coordinate
                if (y < 0) or (y >= 2**z):
                    continue

                filename = os.path.join(x_dir, '%s.png' % str(y))

                # Submit tile to be rendered into the queue
                t = (filename, x, y, z)
                tile_queue.put(t)

    for i in range(process_count):
        renderer = Renderer(tile_queue, config)
        renderer.start()

    tile_queue.join()

if __name__ == "__main__":
    
    #python render_tiles.py tilemill/wards.xml mayor-2011/.tiles/wards/ -89.03 41.07 -87.51 42.50 9 16 2
    parser = argparse.ArgumentParser(description='Render tiles for a given bounding box from a Mapnik2 XML configuration file.')
    parser.add_argument('config', help="Mapnik2 XML configuration file")
    parser.add_argument('tile_dir', help="Destination directory for rendered tiles")
    parser.add_argument('lat_1', type=float, help="Most nortern latitude")
    parser.add_argument('lon_1', type=float, help="Most western longitude")
    parser.add_argument('lat_2', type=float, help="Most southern latitude")
    parser.add_argument('lon_2', type=float, help="Most eastern longitude")
    parser.add_argument('min_zoom', help="Minimum zoom level to render", type=int, default=DEFAULT_MIN_ZOOM)
    parser.add_argument('max_zoom', help="Maximum zoom level to render", type=int, default=DEFAULT_MAX_ZOOM)
    parser.add_argument('process_count', help="Number of rendering processes to create", type=int, default=DEFAULT_PROCESS_COUNT)
    args = parser.parse_args()
    
    bbox = (args.lat_1, args.lon_1,  args.lat_2, args.lon_2)
    
    render_tiles(bbox, args.config, args.tile_dir, args.min_zoom, args.max_zoom, args.process_count)
