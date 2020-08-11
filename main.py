import json
import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from pathlib import Path

path = Path('index.htm')
f = open(path, "r")

last_updated = datetime.fromtimestamp(os.path.getmtime(path))
soup = BeautifulSoup(f, 'html.parser')

activities_html = soup.find_all('div', class_='activity')

# Find athletes
athletes = dict()
for entry in activities_html:
    athlete = entry.find_all('a', class_='entry-athlete')[0]
    athlete_id = athlete.get('href').split('/')[4]
    athlete_name = athlete.text.strip().replace('\nSubscriber', '')
    athletes[athlete_id] = {'id': athlete_id, 'name': athlete_name}

# Find entries
entries = list()
for entry in activities_html:
    athlete = entry.find_all('a', class_='entry-athlete')[0]
    athlete_id = athlete.get('href').split('/')[4]

    activity_id = entry.get('id').split('-')[1]
    datetime_str = entry.find_all('time')[0].get('datetime').replace(' UTC', '')
    datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

    distance_list = entry.find_all('li', title='Distance')
    distance = '0'

    if len(distance_list) > 0:
        distance = distance_list[0].text.replace(' km', '').replace(' m', '')

    duration_list = entry.find_all('li', title='Time')
    duration = timedelta()
    if len(duration_list) > 0:
        for i, e in enumerate(duration_list[0]):
            if i % 2 == 0:
                number = int(e.strip())
                unit = e.next_element.attrs['title']
                if unit == 'hour':
                    duration += timedelta(hours=number)
                if unit == 'minute':
                    duration += timedelta(minutes=number)
                if unit == 'second':
                    duration += timedelta(seconds=number)

    type_class = entry.find_all('span', class_='app-icon')[0].attrs['class']
    type_str = 'unknown'

    if 'icon-run' in type_class:
        type_str = 'run'
    if 'icon-walk' in type_class:
        type_str = 'walk'
    if 'icon-ride' in type_class:
        type_str = 'bike'
    if 'icon-inlineskate' in type_class:
        type_str = 'skate'
    if 'icon-swim' in type_class:
        type_str = 'swim'
    if 'icon-workout' in type_class:
        type_str = 'workout'

    obj = {
        'id': activity_id,
        'athlete_id': athlete_id,
        'datetime': datetime,
        'distance': round(float(distance) * 1000),
        'duration': duration,
        'type': type_str
    }

    entries.append(obj)

for athlete_id, athlete_data in athletes.items():
    activities_per_athlete = list(filter(lambda x: x['athlete_id'] == athlete_id, entries))

    today = datetime.date().today()
    idx = today.weekday() % 7
    last_monday = today - timedelta(idx) - timedelta(weeks=1)
    next_sunday = today + timedelta(7 - idx - 1) - timedelta(weeks=1)

    distance_run = 0
    distance_bike = 0
    distance_other = 0
    total_duration = timedelta()

    for act in activities_per_athlete:
        date = act['datetime'].date()
        if last_monday <= date <= next_sunday:
            distance_this_week = dict()

            type = act['type']
            distance = act['distance']
            duration = act['duration']

            if type == 'run':
                distance_run += distance
            elif type == 'bike':
                distance_bike += distance
            else:
                distance_other += distance

            total_duration += duration

    distance_this_week = {
        'monday': last_monday,
        'sunday': next_sunday,
        'run': distance_run,
        'bike': distance_bike,
        'others': distance_other,
        'total_time': total_duration
    }

    athletes[athlete_id]['activities'] = activities_per_athlete
    athletes[athlete_id]['distance_this_week'] = distance_this_week
    athletes[athlete_id]['can_participate'] = total_duration >= timedelta(hours=3, minutes=30)

data = dict()
data['athletes'] = list(athletes.values())
data['last_updated'] = last_updated


today = datetime.date().today()
idx = today.weekday() % 7
last_monday = today - timedelta(idx) - timedelta(weeks=1)
next_sunday = today + timedelta(7 - idx - 1) - timedelta(weeks=1)

data['date_from'] = last_monday
data['date_to'] = next_sunday

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, default=str, ensure_ascii=False)
