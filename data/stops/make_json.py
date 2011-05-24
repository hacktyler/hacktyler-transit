#!/usr/bin/env python

import csv
import json

stops = [] 

with open('bus-stops.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Fix up types for client
        row['order'] = int(row['order'])
        row['shelter'] = (row['shelter'] == 'TRUE')
        row['sign'] = (row['sign'] == 'TRUE')
        row['flag'] = (row['flag'] == 'TRUE')

        row['latitude'] = float(row['latitude']) if row['latitude'] else None
        row['longitude'] = float(row['longitude'])  if row['longitude'] else None
        
        # Append a few useful attributes
        row['line-slug'] = row['line'].replace(' ', '-').lower()
        row['slug'] = (row['stop_street'] + '_' + row['next_cross_street']).replace(' ', '_').lower()

        stops.append(row)

with open('../../app/web/data/bus-stops.js', 'w') as f:
    f.write('TRANSIT_STOPS = %s' % json.dumps(stops))
