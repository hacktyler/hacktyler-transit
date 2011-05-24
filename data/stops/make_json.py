#!/usr/bin/env python

import csv
import json

lines = {}

with open('bus-stops.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        line = row.pop('line')
        
        # Fix up types for client
        row['order'] = int(row['order'])
        row['shelter'] = (row['shelter'] == 'TRUE')
        row['sign'] = (row['sign'] == 'TRUE')
        row['flag'] = (row['flag'] == 'TRUE')

        row['latitude'] = float(row['latitude']) if row['latitude'] else None
        row['longitude'] = float(row['longitude'])  if row['longitude'] else None

        if line in lines:
            lines[line].append(row)
        else:
            lines[line] = [row]

with open('../../app/web/data/bus-stops.js', 'w') as f:
    f.write('TRANSIT_ROUTES = %s' % json.dumps(lines))
