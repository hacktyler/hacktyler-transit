#!/usr/bin/python

from math import pi,sin,log,exp,atan

import mapnik2

DEG_TO_RAD = pi/180
RAD_TO_DEG = 180/pi

mapnik2.register_fonts('/Library/Fonts/')
mapnik2.register_fonts('/usr/share/fonts')

def minmax (a,b,c):
    a = max(a,b)
    a = min(a,c)
    return a

class GoogleProjection:
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

def render_centered(filename, latitude, longitude, zoom, width=256, height=256, filetype='png256'):
    mmap = mapnik2.Map(width, height)
    mapnik2.load_map(mmap, 'transit.xml', True)
    map_proj = mapnik2.Projection(mmap.srs)

    tile_proj = GoogleProjection()
    x, y = tile_proj.fromLLtoPixel([longitude, latitude], zoom) 

    # Calculate pixel positions of bottom-left & top-right
    half_width = width / 2
    half_height = height / 2
    p0 = (x - half_width, y + half_height)
    p1 = (x + half_width, y - half_height)

    # Convert tile coords to LatLng
    l0 = tile_proj.fromPixelToLL(p0, zoom);
    l1 = tile_proj.fromPixelToLL(p1, zoom);

    # Convert LatLng to map coords
    c0 = map_proj.forward(mapnik2.Coord(l0[0], l0[1]))
    c1 = map_proj.forward(mapnik2.Coord(l1[0], l1[1]))

    # Create bounding box for the render
    bbox = mapnik2.Box2d(c0.x, c0.y, c1.x, c1.y)

    mmap.zoom_to_box(bbox)
    mmap.buffer_size = max([half_width, half_height]) 

    # Render image with default Agg renderer
    image = mapnik2.Image(width, height)
    mapnik2.render(mmap, image)
    image.save(filename, filetype)

if __name__ == "__main__":
    # Tyler lower-left: -95.393,32.2307
    # Tyler upper-right: -95.1928,32.4419
    # Tyler center: -95.301, 32.351
    import csv

    zoom = 16 
    width = 300 
    height = 225 
    filetype = 'png256'

    with open('../data/stops/bus-stops.csv', 'r') as f:
        rows = csv.DictReader(f)

        for row in rows:
            if row['order'] == 'END':
                continue

            if not row['latitude'] or not row['longitude']:
                continue

            lat = float(row['latitude'])
            lon = float(row['longitude'])

            print 'Rendering %s.png' % row['order']
            render_centered('../app/web/images/maps/%s.png' % row['order'], lat, lon, zoom, width, height, filetype)

