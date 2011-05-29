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
                hour, minute = map(int, v.split(':'))

                if is_pm[i]:
                    o.append('%i:%i' % (hour + 12, minute))
                else:
                    if hour < 6:
                        o.append('%i:%i' % (hour + 12, minute))
                        is_pm[i] = True
                    else:
                        o.append(v)

            output.append(o)

    headers = output[0]
    formatted_output = zip(output[0], [','.join(i) for i in zip(*output[1:])])
                    
    with open(os.path.join(OUTPUT_DIR, filename), 'w') as f:
        writer = csv.writer(f)

        writer.writerows(formatted_output)
