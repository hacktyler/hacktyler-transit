#!/usr/bin/env python

import csv
from datetime import date, datetime, time

DUMMY_TIME = date(2100, 12, 31)

LINE = 0
WEEKDAY_SCHEDULE = 12
HAS_OFFICIAL_TIMES = 14

lines = {}

def get_lines():
    line_order = []
    lines = {}

    with open('bus-stops.csv', 'r') as f:
        reader = csv.reader(f)
        header = reader.next()

        for row in reader:
            line = row[LINE]

            if line in lines:
                lines[line].append(row)
            else:
                lines[line] = [row]
                line_order.append(line)

    return header, line_order, lines

def extract_waypoints(stops):
    waypoints = []

    for i, stop in enumerate(stops):
        if stop[HAS_OFFICIAL_TIMES]:
            waypoints.append(i)

    return waypoints

def extract_schedule_from_stop(stop):
    schedule = []

    for t in stop[WEEKDAY_SCHEDULE].split(','):
        hours, minutes = map(int, t.split(':'))
        t = time(hours, minutes)
        schedule.append(datetime.combine(DUMMY_TIME, t))

    return schedule

def calculate_time_deltas(schedule1, schedule2):
    if len(schedule1) != len(schedule2):
        raise ValueError('Got schedules with different lengths.')

    deltas = []

    for i in range(len(schedule1)):
        t1 = schedule1[i]
        t2 = schedule2[i]

        deltas.append(t2 - t1) 

    return deltas

def compute_schedule(stops, waypoints): 
    previous_waypoint = waypoints[0]

    for next_waypoint in waypoints[1:]:
        num_stops = next_waypoint - previous_waypoint
        previous_waypoint_schedule = extract_schedule_from_stop(stops[previous_waypoint])
        next_waypoint_schedule =  extract_schedule_from_stop(stops[next_waypoint])
        deltas = calculate_time_deltas(previous_waypoint_schedule, next_waypoint_schedule)
        increments = [d / num_stops for d in deltas]

        for i in range(num_stops):
            stop = stops[previous_waypoint + i]

            times = []

            for j in range(len(increments)):
                t = previous_waypoint_schedule[j] + (increments[j] * i)
                t = '%s:%s' % (t.hour, str(t.minute).rjust(2 ,'0'))
                times.append(t)

            stop[WEEKDAY_SCHEDULE] = ','.join(times)

            #print stop[1], stop[WEEKDAY_SCHEDULE]

        previous_waypoint = next_waypoint;

def write_lines(header, line_order, lines):
    with open('bus-stops-schedule.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for line in line_order:
            for stop in lines[line]:
                writer.writerow(stop)

if __name__ == "__main__":
    header, line_order, lines = get_lines()

    for line, stops in lines.items():
        waypoints = extract_waypoints(stops)
        compute_schedule(stops, waypoints)

    write_lines(header, line_order, lines)
