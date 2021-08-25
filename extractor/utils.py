import re
import numpy as np
import time as t
import random
from datetime import datetime
from usernames import *
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

# columns!
workout_columns = ['workout_id', 'workout_tp_id', 'workout_strava_id', 'cyclist_id', 'type', 'tags', 'workout_week',
                   'workout_month', 'workout_datetime', 'total_time', 'workout_title', 'cyclist_mass', 'elevation_gain',
                   'elevation_loss', 'elevation_average', 'elevation_maximum', 'elevation_minimum', 'temp_avg',
                   'temp_min', 'temp_max', '_1000_to_1500_m', '_1500_to_2000_m', '_2000_tp_2500_m', '_2500_to_3000_m',
                   '_3000_to_3500_m', 'relative_effort', 'training_load', 'intensity', 'distance', 'energy', 'calories',
                   'if', 'tss_actual', 'tss_calculation_method', 'hidden', 'locked']
workout_hrs_columns = ['workout_id', 'workout_strava_id', 'hr_maximum', 'hr_average', 'hr_5_seconds', 'hr_10_seconds',
                       'hr_12_seconds', 'hr_20_seconds', 'hr_30_seconds', 'hr_1_minute', 'hr_2_minutes', 'hr_5_minutes',
                       'hr_6_minutes', 'hr_10_minutes', 'hr_12_minutes', 'hr_20_minutes', 'hr_30_minutes', 'hr_1_hour',
                       'hr_90_minutes', 'hr_3_hours', 'hr_zone_1', 'hr_zone_2', 'hr_zone_3', 'hr_zone_4', 'hr_zone_5',
                       'hr_zone_1_min', 'hr_zone_2_min', 'hr_zone_3_min', 'hr_zone_4_min', 'hr_zone_5_min']
workout_cadences_columns = ['workout_id', 'workout_strava_id', 'cadence_5_seconds', 'cadence_10_seconds',
                            'cadence_12_seconds', 'cadence_20_seconds', 'cadence_30_seconds', 'cadence_1_minute',
                            'cadence_2_minutes', 'cadence_5_minutes', 'cadence_6_minutes', 'cadence_10_minutes',
                            'cadence_12_minutes', 'cadence_20_minutes', 'cadence_30_minutes', 'cadence_1_hour',
                            'cadence_90_minutes', 'cadence_3_hours', 'cadence_maximum', 'cadence_average']
workout_powers_columns = ['workout_id', 'workout_strava_id', 'power_maximum', 'power_average', 'normalized_power',
                          'power_5_seconds', 'power_10_seconds', 'power_12_seconds', 'power_20_seconds',
                          'power_30_seconds', 'power_1_minute', 'power_2_minutes', 'power_5_minutes', 'power_6_minutes',
                          'power_10_minutes', 'power_12_minutes', 'power_20_minutes', 'power_30_minutes',
                          'power_1_hour', 'power_90_minutes', 'power_3_hours', 'power_zone_1', 'power_zone_2',
                          'power_zone_3', 'power_zone_4', 'power_zone_5', 'power_zone_6', 'power_zone_7',
                          'power_zone_1_min', 'power_zone_2_min', 'power_zone_3_min', 'power_zone_4_min',
                          'power_zone_5_min', 'power_zone_6_min', 'power_zone_7_min']
workout_speeds_columns = ['workout_id', 'workout_strava_id', 'speed_maximum', 'speed_average', 'speed_5_seconds',
                          'speed_10_seconds', 'speed_12_seconds', 'speed_20_seconds', 'speed_30_seconds',
                          'speed_1_minute', 'speed_2_minutes', 'speed_5_minutes', 'speed_6_minutes', 'speed_10_minutes',
                          'speed_12_minutes', 'speed_20_minutes', 'speed_30_minutes', 'speed_1_hour',
                          'speed_90_minutes', 'speed_3_hours', 'speed_zone_1', 'speed_zone_2', 'speed_zone_3',
                          'speed_zone_4', 'speed_zone_5', 'speed_zone_6', 'speed_zone_7', 'speed_zone_1_min',
                          'speed_zone_2_min', 'speed_zone_3_min', 'speed_zone_4_min', 'speed_zone_5_min',
                          'speed_zone_6_min', 'speed_zone_7_min']


def log(msg,level='INFO', id = ''):

    try:
        msg=f'{level} {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {msg}\n'
        print(f'{msg}')
        with open(f"log_{id}.txt",'a+') as f:
            f.write(msg)
        with open(f"S:/log_{id}.txt",'a+') as f:
            f.write(msg)
    except Exception as err:
        pass

def valid_rider_url(url):
    pattern = re.compile("https://www.strava.com/[a-zA-Z]+/[0-9]+$")
    found = pattern.search(url)
    if not found:
        return False
    return True


def to_hours(time_string):
    time = time_string.split(':')
    total = 0
    for i in range(len(time)):
        total += int(re.sub('\D', '', time[i]))/(60**i)
    return total


def to_seconds(time_string):
    time = time_string.split(':')
    total = 0
    for i in range(len(time)):
        total += int(re.sub('\D', '', time[i]))*(60**(len(time) - i - 1))
    return total


def extract_points_from_graph(soup):
    svg = soup.find_all('defs')
    y_offset = float(svg[0].find('rect')['y'])
    height = float(svg[0].find('rect')['height']) + y_offset
    width = float(svg[0].find('rect')['width'])

    ticks = soup.find_all('g', {'class': "tick"})
    ticks = list(map(lambda x: [x['transform'].replace("translate", "")[1:-1], x.find('text').text], ticks))
    ticks = list(map(lambda x: [x[0].split(','), x[1]], ticks))

    x_ticks = [x for x in ticks if 'mi' in x[1]][:7]
    x_single_tick_size = float(x_ticks[1][0][0])
    miles_single_tick_size = float(x_ticks[1][1][:-3])
    ratio_x = miles_single_tick_size / x_single_tick_size

    y_ticks = [x for x in ticks if 'ft' in x[1]]
    y_single_tick_size = float(y_ticks[0][0][1]) - float(y_ticks[1][0][1])
    feet_single_tick_size = float(y_ticks[1][1][:-3].replace(",", "")) - float(y_ticks[0][1][:-3].replace(",", ""))

    minimum_feet_tick = float(y_ticks[0][1][:-3].replace(",", ""))

    ratio_y = feet_single_tick_size / y_single_tick_size

    all_points = soup.find('path', {'id' : 'line'})['d'].split(',')[1:-1]
    all_points = [x.split('L') for x in all_points]
    all_points = [[height - float(x[0]), float(x[1])] for x in all_points]
    all_points = [[(x[0]*ratio_y) + minimum_feet_tick, x[1]*ratio_x] for x in all_points]
    return all_points


def extract_mean_max_metrics(soup):

    # hr_5_seconds, hr_10_seconds, hr_12_seconds, hr_20_seconds, hr_30_seconds, hr_1_minute, hr_5_minutes, hr_6_minutes, hr_10_minutes
    #all_points = extract_points_from_graph(soup)
    axis = soup.find('g', {'class':'axis xaxis'})
    ticks = axis.find_all('g', {'class': 'tick'})
    seconds_translation = []
    for tick in ticks:
        time = list(reversed(tick.find('text').text.replace('s', '').split(':')))
        translation = float(tick['transform'].replace('translate', '').replace('(', '').replace(')', '').split(',')[0])
        seconds = 0
        # calculate seconds
        for i in range(0, len(time)):
            seconds += int(time[i]) * 60**i
        seconds_translation.append((seconds, translation))
    single_sec_interval = (seconds_translation[1][0] - seconds_translation[0][0]), (seconds_translation[1][1] - seconds_translation[0][1])

    total_seconds = 0
    width_figure = 696
    height_figure = 70
    one_sec_width = single_sec_interval[1] / single_sec_interval[0]
    total_seconds = width_figure / one_sec_width

    def mean_metrics(points, seconds):
        current_interval = []
        max_ = []
        for point in points:
            if len(current_interval) == seconds:
                max_.append(np.mean(current_interval))
                current_interval = []
            else:
                current_interval.append(point[0])
        return np.max(max_)

    def create_points(box_name, graph_name, normalize = 1):
        chart = soup.find('div', {'class': 'base-chart'})
        chart_height = float(chart.svg['height'])
        boxes = soup.find_all('g', {'class': 'label-box'})
        translations = []

        for box in boxes:

            translation = float(box['transform'].replace('translate', '').replace('(', '').replace(')', '').replace(' ', '').split(',')[-1])
            translations.append(translation)

        point_box = []
        i = -1
        for box in boxes:
            label = box.find('text', {'class': 'static-label-box label'}).text
            i += 1
            if not label == box_name:
                continue
            max_v = float(box.find('text', {'class': 'static-label-box top'}).text.replace(',', ''))
            low_v = float(box.find('text', {'class': 'static-label-box bottom'}).text.replace(',', ''))
            begin_translation = boxes[i]

            if i+1 < len(boxes):
                end_translation = translations[i+1] - 1
            else:
                end_translation = translations[i] + height_figure - 1

            point_box.append(begin_translation)
            point_box.append(end_translation)
            point_box.append(low_v)
            point_box.append(max_v)
            break

        points = soup.find('g', {'id':graph_name}).find('path')['d'].split(',')[2:-1]
        points = [x.split('L') for x in points]
        points = [[float(x[0]), float(x[1])] for x in points]
        begin_translation = point_box[0]
        end_translation = point_box[1]
        lowest_value = point_box[2]
        maximum_value = point_box[3]
        value_range = maximum_value - lowest_value
        original_points = []

        for point in points:
            calculated_point_y = ((end_translation - point[0])/height_figure * value_range) + lowest_value
            calculated_point_x = round((point[1]/width_figure)*total_seconds)
            original_points.append((calculated_point_y, calculated_point_x))
        original_points = [(point[0]*normalize, point[1]) for point in original_points]
        points = []
        values = []
        for i in range(0, len(original_points)-1):

            point1 = original_points[i]
            point2 = original_points[i+1]

            points.append(point1)

            seconds = point2[1] - point1[1]
            point_interval = point2[0] - point1[0]
            increment = point_interval / seconds
            for j in range(1, seconds):
                new_point = (point1[0] + increment*j)
                points.append((new_point, point1[1]+j))
                values.append(new_point)

        return points, np.mean(values), np.max(values)

    dic = {}
    titles = {'5_seconds': 5,
              '10_seconds': 10,
              '12_seconds': 12,
              '20_seconds': 20,
              '30_seconds': 30,
              '1_minute': 60,
              '2_minutes': 120,
              '5_minutes': 300,
              '6_minutes': 360,
              '10_minutes': 600,
              '12_minutes': 720,
              '20_minutes': 1200,
              '30_minutes': 1800,
              '1_hour': 3600,
              '90_minutes': 5400,
              '3_hours': 10800
              }

    try:
        temp, mean_temp, max_temp = create_points('Temperature' ,'temp')
    except:
        temp = [(0, 0)]

    dic['temp_min'] = min(temp, key = lambda x: x[0])[0]
    dic['temp_max'] = max(temp, key = lambda x: x[0])[0]

    try:
        speed, mean_speed, max_speed = create_points('Speed' ,'velocity_smooth', normalize = 0.44704)
    except:
        speed, mean_speed, max_speed = [], None, None

    dic[f'speed_average'] = mean_speed
    dic[f'speed_maximum'] = max_speed

    try:
        watts, mean_watts, max_watts = create_points('Est Power', 'watts_calc')
    except:
        try:
            watts, mean_watts, max_watts = create_points('Power', 'watts')
        except:
            watts, mean_watts, max_watts = [], None, None
    dic[f'power_average'] = mean_watts
    dic[f'power_maximum'] = max_watts

    try:
        heart_rate, mean_heart_rate, max_heart_rate = create_points('Heart Rate','heartrate')
    except:
        heart_rate, mean_heart_rate, max_heart_rate = [], None, None
    dic[f'hr_average'] = mean_heart_rate
    dic[f'hr_maximum'] = max_heart_rate

    try:
        cadence, mean_cadence, max_cadence = create_points('Cadence', 'cadence')
    except:
        cadence, mean_cadence, max_cadence = [], None, None
    dic[f'cadence_average'] = mean_cadence
    dic[f'cadence_maximum'] = max_cadence

    for key, value in titles.items():
        try:
            metric = mean_metrics(speed, value)
        except:
            metric = None
        dic[f'speed_{key}'] = metric

    for key, value in titles.items():
        try:
            metric = mean_metrics(watts, value)
        except:
            metric = None
        dic[f'power_{key}'] = metric

    for key, value in titles.items():
        try:
            metric = mean_metrics(heart_rate, value)
        except:
            metric = None
        dic[f'hr_{key}'] = metric


    for key, value in titles.items():
        try:
            metric = mean_metrics(cadence, value)
        except:
            metric = None
        dic[f'cadence_{key}'] = metric

    return dic


def extract_graph_elevation_distance(soup):
    # Graph data (height...)
    all_points = extract_points_from_graph(soup)

    def calculate_distance_for_height(points, min_dis, max_dis):
        in_range = False
        relevent_points = []
        for x, y in points:

            if x >= min_dis and x < max_dis:
                if not in_range:
                    relevent_points.append([])
                    in_range = True
                relevent_points[-1].append((x,y))
            else:
                in_range = False
        total_distance = 0
        for section in relevent_points:
            first_point = section[0]
            end_point = section[-1]
            total_distance += end_point[1] - first_point[1]

        return total_distance

    def calculate_elevation_gain_loss(points):

        elevation_gain = 0
        elevation_loss = 0
        max_ = float('-inf')
        min_ = float('inf')
        elevating_now = 0
        up = True
        for i in range(1, len(points)):
            prev = points[i-1][0] * 0.3048 # ft to meter
            curr = points[i][0] * 0.3048 # ft to meter

            if prev > curr:
                if up:
                    min_ = min(elevating_now, min_)
                    elevating_now = 0
                up = False
                elevation_loss += (prev - curr)
                elevating_now += (prev - curr)
            elif prev < curr:
                if not up:
                    max_ = max(elevating_now, max_)
                    elevating_now = 0
                up = True
                elevation_gain += (curr - prev)
                elevating_now += (curr - prev)


        return elevation_gain, elevation_loss, min_, max_

    def calculate_elevation_mean_max_min(points):
        Y = []
        for point in points:
            Y.append(point[0])
        return np.min(Y), np.max(Y), np.mean(Y)


    # Calculate the props
    # workouts table
    dic = {}
    dic['_1000_to_1500_m'] = calculate_distance_for_height(all_points, 1000, 1500)
    dic['_1500_to_2000_m'] = calculate_distance_for_height(all_points, 1500, 2000)
    dic['_2000_tp_2500_m'] = calculate_distance_for_height(all_points, 2000, 2500)
    dic['_2500_to_3000_m'] = calculate_distance_for_height(all_points, 2500, 3000)
    dic['_3000_to_3500_m'] = calculate_distance_for_height(all_points, 3000, 3500)

    elevation_gain, elevation_loss, min_, max_ = calculate_elevation_gain_loss(all_points)
    dic['elevation_gain'] = elevation_gain
    dic['elevation_loss'] = elevation_loss
    #     dic['elevation_minimum'] = min_
    #     dic['elevation_maximum'] = max_

    min_, max_, mean_ = calculate_elevation_mean_max_min(all_points)
    dic['elevation_minimum'] = min_
    dic['elevation_maximum'] = max_
    dic['elevation_average'] = mean_

    return dic


def divide_to_tables(data, rider_id):

    #workout
    workout_row = {}
    workout_hrs_row = {}
    workout_cadences_row = {}
    workout_powers_row = {}
    workout_speeds_row = {}
    key_not_found = []

    workout_row['cyclist_id'] = rider_id

    for key, value in data.items():
        key = key.lower()
        found = False
        if key in workout_columns:
            workout_row[key] = value
            found = True
        if key in workout_hrs_columns:
            workout_hrs_row[key] = value
            found = True
        if key in workout_cadences_columns:
            workout_cadences_row[key] = value
            found = True
        if key in workout_powers_columns:
            workout_powers_row[key] = value
            found = True
        if key in workout_speeds_columns:
            workout_speeds_row[key] = value
            found = True
        if not found:
            key_not_found.append(key)

    for key in workout_columns:
        if key not in workout_row:
            workout_row[key] = None

    for key in workout_hrs_columns:
        if key not in workout_hrs_row:
            workout_hrs_row[key] = None

    for key in workout_cadences_columns:
        if key not in workout_cadences_row:
            workout_cadences_row[key] = None

    for key in workout_powers_columns:
        if key not in workout_powers_row:
            workout_powers_row[key] = None

    for key in workout_speeds_columns:
        if key not in workout_speeds_row:
            workout_speeds_row[key] = None

    return workout_row, workout_hrs_row, workout_cadences_row, workout_powers_row, workout_speeds_row, key_not_found
