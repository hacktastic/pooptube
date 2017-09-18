#!/usr/bin/env python3

import sys
import yaml
import re
from datetime import time
import time as t
import subprocess
import logging

schedule_filename = '/root/.config/pianobar/schedule.yml'
pianobar_fifo = '/tmp/pianobar'
FORMAT = '[%(asctime)s] %(message)s'
logging.basicConfig(datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, format=FORMAT)

def main():
    event = sys.argv[1]
    lines = sys.stdin.readlines()
    fields = dict([line.strip().split("=", 1) for line in lines])
    logging.info(event)
    #for k,v in sorted(fields.items()):
    #    logging.info (''.join(k, ':', v))
    if event in ('usergetstations', 'songfinish'):
        stations = get_stations(fields)
        #logging.info(stations)
        current_station_name = fields.get('stationName')
        desired_station_name = what_station_should_be_playing_now()
        station_num = stations.get(desired_station_name)

        if current_station_name != desired_station_name:
            if event == 'usergetstations':
                send_message_to_proc(str(station_num))
            else:
                switch_station(station_num)
        else:
            logging.info('No need to change stations yet.')

def switch_station(station_num):
    logging.info('switching station to: {}'.format(station_num))
    send_message_to_proc('s' + str(station_num))

def send_message_to_proc(msg):
    subprocess.call('echo "{0}" > {1}'.format(msg, pianobar_fifo), shell=True)

def get_stations(fields):
    """
    get_stations() takes in fields from pianobar and returns a dict of station names to station numbers
    """
    stations = dict()
    for k,v in sorted(fields.items()):
        match = re.match('^station([0-9]+)', k)
        if match:
            match_groups = match.groups()
            if match_groups:
                station_num = match_groups[0]
                stations[v] = station_num
    return stations

def get_timestamp(naive_time):
    """
    get_timestamp() takes in a timestamp string and converts it to a datetime.time object.
    Acceptable formats include "1 PM" "13:00" "01:00 PM" and "13:00 PM"
    """
    hour, minute, daypart = re.search('([0-9]?[0-9]):?([0-9][0-9])? ?(AM|PM)?', naive_time).groups()
    # if the timestamp has "PM", add 12 to the hour value
    if hour != None:
        hour = int(hour)
        if daypart == 'PM' and hour < 12:
            hour += 12
    # if no minute value found, set minute=0; otherwise, convert minute to int
    if minute != None:
        minute = int(minute)
    else:
        minute = 0
    return time(hour, minute)

def get_current_time():
    """
    get_current_time() returns the current time as a datetime.time object
    """
    return time(*[int(x) for x in t.strftime('%H,%M,%S').split(',')])

def get_schedule(schedule_filepath):
    """
    get_schedule() opens a yaml config file and returns a dict of start times to station names
    """
    schedule = dict()
    f = open(schedule_filepath, 'r')
    y = yaml.load(f.read())
    for item in y.get('schedule'):
        schedule[get_timestamp(item.get('startTime'))] = item.get('stationName')
    return schedule

def what_station_should_be_playing_now():
    """
    what_station_should_be_playing_now() returns the name of the station that should be playing right now
    """
    current_time = get_current_time()
    schedule = get_schedule(schedule_filename)
    start_times = sorted(schedule.keys())

    # iterate over all the start times by index
    for i in range(len(start_times)):
        this_time = start_times[i]

        # start_time indexes except the last one
        if i < len(start_times)-1:
            next_time = start_times[i+1]
            if this_time <= current_time <= next_time:
                station_name = schedule.get(this_time)
                return station_name
        # if we haven't found a start_time that fits yet, use the latest start time
        else:
            station_name = schedule.get(this_time)
            return station_name

if __name__ == '__main__':
    main()

