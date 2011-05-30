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
        row['shelter'] = (row['shelter'] == 'TRUE')
        row['sign'] = (row['sign'] == 'TRUE')
        row['flag'] = (row['flag'] == 'TRUE')

        row['latitude'] = float(row['latitude']) if row['latitude'] else None
        row['longitude'] = float(row['longitude'])  if row['longitude'] else None

        def format_time(t):
            h, m = map(int, t.split(':'))
            if h > 12:
                return '%i:%i PM' % (h - 12, m)
            elif h == 12:
                return '%i:%i PM' % (h, m)
            else:
                return '%i:%i AM' % (h, m)

        row['weekday_schedule'] = map(format_time, row['weekday_schedule'].split(','))
        print row['weekday_schedule']
        
        # Append a few useful attributes
        row['line-slug'] = row['line'].replace(' ', '-').lower()
        
        slug = (row['stop_street'] + '_' + row['next_cross_street']).replace(' ', '_').lower()

        # Prevent slug name collisions
        if slug in slugs:
            n = 2

            while '%s_%i' % (slug, n) in slugs:
                n += 1

            slug = '%s_%i' % (slug, n)

        slugs.append(slug)
        row['slug'] = slug

        stops.append(row)

with open('../../app/web/data/bus-stops.js', 'w') as f:
    f.write('TRANSIT_STOPS = %s' % json.dumps(stops))
