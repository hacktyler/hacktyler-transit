#!/usr/bin/env python

import csv
import json

stops = [] 
slugs = []

with open('bus-stops-schedule.csv', 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        # Don't serialize endpoints (they duplicate first stop)
        if row['order'] == 'END':
            continue

        # Fix up types for client
        row['order'] = int(row['order'])
        row['estimated_location'] = (row['estimated_location'] == 'TRUE')

        row['latitude'] = float(row['latitude']) if row['latitude'] else None
        row['longitude'] = float(row['longitude'])  if row['longitude'] else None

        def format_time(t):
            h, m = map(int, t.split(':'))
            if h > 12:
                return '%i:%02i PM' % (h - 12, m)
            elif h == 12:
                return '%i:%02i PM' % (h, m)
            else:
                return '%i:%02i AM' % (h, m)

        row['weekday_schedule'] = map(format_time, row['weekday_schedule'].split(','))
        
        # Append a few useful attributes
        row['line-slug'] = row['line'].lower() + '-line-' + row['direction'].lower()

        stops.append(row)

with open('../../app/web/data/bus-stops.js', 'w') as f:
    f.write('TRANSIT_STOPS = %s' % json.dumps(stops))
