#!/usr/bin/env python

"""
Bus service never starts earlier than 6:00 AM.
Bus service never ends later than 8:30 PM.
"""

import csv
import os

INPUT_DIR = 'bus_routes_weekday'
OUTPUT_DIR = 'bus_routes_weekday_clean'

try:
    os.mkdir(OUTPUT_DIR)
except OSError:
    pass

for filename in os.listdir(INPUT_DIR):
    path = os.path.join(INPUT_DIR, filename)

    buffered = [] 
    output = []

    with open(path, 'rU') as f:
        for line in f:
            buffered.append(line.replace('\x00', ' '))

        reader = csv.reader(buffered)
        headers = reader.next()

        is_pm = [False for r in headers]

        output.append(headers)

        for row in reader:
            o = [] 

            for i, v in enumerate(row):
                if is_pm[i]:
                    o.append('%s PM' % v)
                else:
                    hour = int(v.split(':')[0])

                    if hour == 12 or hour < 6:
                        o.append('%s PM' % v)
                        is_pm[i] = True
                    else:
                        o.append('%s AM' % v)

            output.append(o)
                    
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        writer = csv.writer(f)

        writer.writerows(output)
