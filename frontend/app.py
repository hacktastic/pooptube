from flask import Flask, render_template, request
import yaml
import re
from datetime import time

app = Flask(__name__)

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

def convert_timestamp(timestamp):
    hour = timestamp.hour
    minute = timestamp.minute
    daypart = 'AM'
    if hour == 12:
        daypart = 'PM'
    elif hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
        daypart = 'PM'
    return hour, minute, daypart

@app.route('/')
def hello_world():
    building = '13'
    floor = '1'
    gender = 'Mens'
    num = '1'
    schedule = []
    stations = []
    schedule_y = yaml.load(open('schedule.yml').read()).get('schedule')
    for item in schedule_y:
        start_hour, start_minute, start_daypart = convert_timestamp(get_timestamp(item.get('startTime')))
        station_name = item.get('stationName')
        schedule.append({
            'station_name': station_name,
            'start_hour': start_hour,
            'start_minute': start_minute,
            'start_daypart': start_daypart,
        })
        stations.append(station_name)
    return render_template('index.html',
        building=building,
        floor=floor,
        gender=gender,
        num=num,
        schedule=schedule,
        stations=stations,
    )

@app.route('/new_schedule', methods=['POST'])
def new_schedule():
    schedule = dict()
    print(request.form)
    for k,v in request.form.iteritems():
        keyword, num = re.search('([A-Za-z]+)-([0-9]+)', k).groups()
        if not schedule.get(num):
            schedule[num] = dict()
        schedule[num][keyword] = v
    schedule_y = {'schedule': []}
    for item in schedule.itervalues():
        schedule_y['schedule'].append({
            'stationName': str(item.get('station')),
            'startTime': '{:02d}:{:02d} {}'.format(int(item.get('hour')), int(item.get('minute')), item.get('daypart'))
        })
    with open('sample_schedule.yml', 'w') as output:
        output.write(yaml.dump(schedule_y))
    return hello_world()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
