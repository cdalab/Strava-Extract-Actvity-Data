import argparse
import os
import re
import traceback
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy as np
from datetime import datetime
from pathlib import Path
import pandas as pd
import random
import requests
import time as t
from consts import *


def setting_up():
    from consts import USERS





    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', type=str)
    parser.add_argument('-if', '--input-file', type=str)
    parser.add_argument('-of', '--output-file', type=str)
    parser.add_argument('-li', '--low-limit-index', type=int)
    parser.add_argument('-hi', '--high-limit-index', type=int)
    parser.add_argument('-r', '--riders', type=str)
    parser.add_argument('-rl', '--riders-low-index', type=int)
    parser.add_argument('-rh', '--riders-high-index', type=int)
    parser.add_argument('-t', '--num-of-threads', type=int)
    parser.add_argument('-o', '--overwrite-mode', type=int)
    parser.add_argument('-w', '--week-range', type=str)
    parser.add_argument('-u', '--users-range', type=str)
    args = parser.parse_args()
    args_dict = dict(
        command=args.command,
        input_file=args.input_file,
        output_file=args.output_file,
        low_limit_index=args.low_limit_index,
        high_limit_index=args.high_limit_index,
        riders_low_index=args.riders_low_index,
        riders_high_index=args.riders_high_index,
        riders=json.loads(args.riders) if args.riders is not None else None,
        num_of_threads=args.num_of_threads,
        overwrite_mode=args.overwrite_mode,
        week_range=args.week_range,
    )

    if args.command is None:
        raise ValueError('Cannot run the job without a command')
    if args.users_range is not None:
        s_idx, e_idx = None,None
        users_input = json.loads(args.users_range)
        if ('start' in users_input):
            s_idx=users_input['start']
            if ('step' in users_input):
                e_idx = s_idx + users_input['step']
            elif ('end' in users_input):
                e_idx =users_input['end']
            else:
                e_idx = len(USERS)
        else:
            raise ValueError('User range input is not valid.')
        USERS = USERS[s_idx:e_idx]


    ip_addrs = requests.get('http://ipinfo.io/json').json()['ip']
    id = f"{ip_addrs}_{args.command}"
    args_dict['id'] = id
    log(f'', id=id)
    log(f'', id=id)
    log(f'====================================================================', id=id)
    if args.users_range is not None:
        log(f'USERS[{s_idx}:{e_idx}]', id=id)
    log(f'{args_dict}', id=id)
    log(f'', id=id)
    log(f'', id=id)

    return args_dict


# https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def read_from_html(parent_dir, html_file):
    with open(f"{parent_dir}/{html_file}", encoding='utf-8') as f:
        html_content = f.read()
    return html_content


def write_to_html(parent_dir, html_file, content):
    Path(parent_dir).mkdir(parents=True, exist_ok=True)
    with open(f"{parent_dir}/{html_file}.html", "w+", encoding='utf-8') as f:
        f.write(content)


def log(msg, type='INFO', id='', debug=DEBUG):
    Path('./log/').mkdir(parents=True, exist_ok=True)
    type = type.upper()
    if LOG_LEVEL_DICT[type] <= LOG_LEVEL_DICT[LOG_LEVEL]:
        if type == 'ERROR':
            msg += f' ERROR DETAILS: {traceback.format_exc()}'
        msg = f'{type}\t{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\t{msg}\n'
        with open(f'./log/{type}_{id}.log', 'a+') as f:
            f.write(msg)
        if debug:
            print(f'{msg}'.replace("\n", ""))


def error_handler(function, params, id=''):
    error_df_path = f'./log/ERROR_DF_{id}.csv'
    for p in params.keys():
        params[p] = str(params[p]).replace('\n', '')
    df = pd.DataFrame([params])
    df['function'] = function
    if not os.path.exists(error_df_path):
        df.to_csv(error_df_path, index=False, header=True)
    df.to_csv(error_df_path, mode='a', index=False, header=False)


def get_overwrite_pred(dir, files, overwrite_mode):
    overwrite = (overwrite_mode is not None) and overwrite_mode
    files_exists = True
    for file in files:
        files_exists = files_exists and os.path.exists(f"{dir}/{file}.html")
    return overwrite or (not files_exists)


def download_files_wrapper(func):
    def wrap(self, msg, dir, files, overwrite_mode, *args, **kwargs):
        if get_overwrite_pred(dir, files, overwrite_mode):
            files_content = func(self, *args, **kwargs)
            log(msg, id=self.id)
            for file in files_content.keys():
                write_to_html(dir, file, files_content[file])

    return wrap


def timeout_wrapper(func):
    def wrap(self, msg=ERROR_DEFAULT_MSG, *args, **kwargs):
        trials = 0
        while trials < TIMEOUT:
            try:
                params = kwargs
                result = func(self, *args, **kwargs)
                return result
            except:
                trials += 1
                for err in self.browser.get_log('browser'):
                    if err['source'] == 'network':
                        current_url = self.browser.current_url
                        err_url = err['message'].split(' - ')[0]
                        self.browser.get(err_url)
                        self._is_valid_html(err_url)
                        self.browser.get(current_url)
                if trials == TIMEOUT:
                    parent_dir = 'log/problematic_htmls'
                    file_name = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
                    Path(parent_dir).mkdir(parents=True, exist_ok=True)
                    write_to_html(parent_dir, file_name, self.browser.page_source)
                    log(msg, 'ERROR', id=self.id)
                    error_handler(func.__name__, params, id=self.id)

    return wrap


def driver_wrapper(func):
    def wrap(self, *args, **kwargs):
            user = self._open_driver()
            err_metrics = f"Metrics are not as expected in user {user}"
            self.validate_units(err_metrics)
            result = func(self, *args, **kwargs)
            return result

    return wrap


def valid_rider_url(url):
    pattern = re.compile("https://www.strava.com/[a-zA-Z]+/[0-9]+$")
    found = pattern.search(url)
    if not found:
        return False
    if ('pros' and 'athletes') not in url:
        return False
    return True


def check_int(sting):
    return re.match(r"[-+]?\d+(\.0*)?$", sting) is not None


def check_float(sting):
    return re.match(r'^-?\d+(?:\.\d+)$', sting) is not None


def to_hours(time_string):
    time = time_string.split(':')
    total = 0
    for i in range(len(time)):
        total += int(re.sub('\D', '', time[i])) / (60 ** i)
    return total


def to_seconds(time_string):
    time = time_string.split(':')
    total = 0
    for i in range(len(time)):
        total += int(re.sub('\D', '', time[i])) * (60 ** (len(time) - i - 1))
    return total


def extract_points_from_graph(soup):
    '''
    Extract the raw points from graph and convert from pixels to original point values
    '''

    svg = soup.find_all('defs')
    y_offset = float(svg[0].find('rect')['y'])
    height = float(svg[0].find('rect')['height']) + y_offset
    width = float(svg[0].find('rect')['width'])

    ticks = soup.find_all('g', {'class': "tick"})
    ticks = list(map(lambda x: [x['transform'].replace("translate", "")[1:-1], x.find('text').text], ticks))
    ticks = list(map(lambda x: [x[0].split(','), x[1]], ticks))

    x_ticks = [x for x in ticks if 'mi' in x[1]][:7]
    x_single_tick_size = float(x_ticks[1][0][0])  # the width between two ticks
    miles_single_tick_size = float(x_ticks[1][1][:-3])  # the value between two ticks
    ratio_x = miles_single_tick_size / x_single_tick_size  # ratio between width and value

    y_ticks = [x for x in ticks if 'ft' in x[1]]
    y_single_tick_size = float(y_ticks[0][0][1]) - float(y_ticks[1][0][1])  # the height between two ticks
    feet_single_tick_size = float(y_ticks[1][1][:-3].replace(",", "")) - float(
        y_ticks[0][1][:-3].replace(",", ""))  # the value between two ticks

    minimum_feet_tick = float(
        y_ticks[0][1][:-3].replace(",", ""))  # the minimum value of y coordinates to find the starting point

    ratio_y = feet_single_tick_size / y_single_tick_size  # ratio between height and value

    all_points = soup.find('path', {'id': 'line'})['d'].split(',')[1:-1]
    all_points = [x.split('L') for x in all_points]
    all_points = [[height - float(x[0]), float(x[1])] for x in all_points]
    all_points = [[(x[0] * ratio_y) + minimum_feet_tick, x[1] * ratio_x] for x in
                  all_points]  # map pixels into original values according to ratios
    return all_points


def extract_mean_max_metrics(soup):
    '''
    To calculate the mean, max metrics we need to fill missing points.
    for example if there are points in x coordinates [1,3,12, 19]
    we need to have [1, 2, 3, 4, ... , 19]
    The method uses a a simple linear filler: y=mx+b. find the m and b between two points and fill the rest missing points    
    '''
    # hr_5_seconds, hr_10_seconds, hr_12_seconds, hr_20_seconds, hr_30_seconds, hr_1_minute, hr_5_minutes, hr_6_minutes, hr_10_minutes
    # all_points = extract_points_from_graph(soup)
    axis = soup.find('g', {'class': 'axis xaxis'})
    ticks = axis.find_all('g', {'class': 'tick'})
    seconds_translation = []
    for tick in ticks:
        time = list(reversed(tick.find('text').text.replace('s', '').split(':')))
        translation = float(tick['transform'].replace('translate', '').replace('(', '').replace(')', '').split(',')[0])
        seconds = 0
        # calculate seconds
        for i in range(0, len(time)):
            seconds += int(time[i]) * 60 ** i
        seconds_translation.append((seconds, translation))
    single_sec_interval = (seconds_translation[1][0] - seconds_translation[0][0]), (
            seconds_translation[1][1] - seconds_translation[0][1])

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

    def create_points(box_name, graph_name, normalize=1):
        chart = soup.find('div', {'class': 'base-chart'})
        chart_height = float(chart.svg['height'])
        boxes = soup.find_all('g', {'class': 'label-box'})
        translations = []

        for box in boxes:
            translation = float(
                box['transform'].replace('translate', '').replace('(', '').replace(')', '').replace(' ', '').split(',')[
                    -1])
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

            if i + 1 < len(boxes):
                end_translation = translations[i + 1] - 1
            else:
                end_translation = translations[i] + height_figure - 1

            point_box.append(begin_translation)
            point_box.append(end_translation)
            point_box.append(low_v)
            point_box.append(max_v)
            break

        points = soup.find('g', {'id': graph_name}).find('path')['d'].split(',')[2:-1]
        points = [x.split('L') for x in points]
        points = [[float(x[0]), float(x[1])] for x in points]
        begin_translation = point_box[0]
        end_translation = point_box[1]
        lowest_value = point_box[2]
        maximum_value = point_box[3]
        value_range = maximum_value - lowest_value
        original_points = []

        for point in points:
            calculated_point_y = ((end_translation - point[0]) / height_figure * value_range) + lowest_value
            calculated_point_x = round((point[1] / width_figure) * total_seconds)
            original_points.append((calculated_point_y, calculated_point_x))
        original_points = [(point[0] * normalize, point[1]) for point in original_points]
        points = []
        values = []
        for i in range(0, len(original_points) - 1):

            point1 = original_points[i]
            point2 = original_points[i + 1]

            points.append(point1)

            seconds = point2[1] - point1[1]
            point_interval = point2[0] - point1[0]
            increment = point_interval / seconds
            for j in range(1, seconds):
                new_point = (point1[0] + increment * j)
                points.append((new_point, point1[1] + j))
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
        temp, mean_temp, max_temp = create_points('Temperature', 'temp')
        dic['temp_min'] = min(temp, key=lambda x: x[0])[0]
        dic['temp_max'] = max(temp, key=lambda x: x[0])[0]
    except:
        temp = [(None, None)]

    try:
        speed, mean_speed, max_speed = create_points('Speed', 'velocity_smooth', normalize=0.44704)
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
        heart_rate, mean_heart_rate, max_heart_rate = create_points('Heart Rate', 'heartrate')
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
    all_points = extract_points_from_graph(soup)  # Returns all points from graph after calculating the original value

    def calculate_distance_for_height(points, min_dis, max_dis):
        # Calculate the total distance traveled for specific height range (1000_to_1500 for example)
        in_range = False
        relevant_points = []
        for x, y in points:
            if x >= min_dis and x < max_dis:
                if not in_range:
                    relevant_points.append([])
                    in_range = True
                relevant_points[-1].append((x, y))
            else:
                in_range = False
        total_distance = 0
        for section in relevant_points:
            first_point = section[0]
            end_point = section[-1]
            total_distance += end_point[1] - first_point[1]
        return total_distance

    def calculate_elevation_gain_loss(points):
        # Calculate the elevation gain and loss of graph
        # by comparing the previous point with current.
        elevation_gain = 0
        elevation_loss = 0
        max_ = float('-inf')
        min_ = float('inf')
        elevating_now = 0
        up = True  # Flag to see if the direction of previous points was an elevation to find the minimum and maximum elevations
        for i in range(1, len(points)):
            prev = points[i - 1][0] * 0.3048  # ft to meter
            curr = points[i][0] * 0.3048  # ft to meter

            if prev > curr:  # Case where there is a decline - elevation loss
                if up:
                    min_ = min(elevating_now, min_)
                    elevating_now = 0  # reset the current elevation
                up = False
                elevation_loss += (prev - curr)
                elevating_now += (prev - curr)
            elif prev < curr:  # Case where there is an increase - elevation gain
                if not up:
                    max_ = max(elevating_now, max_)
                    elevating_now = 0  # reset the current elevation
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
    dic['_2000_to_2500_m'] = calculate_distance_for_height(all_points, 2000, 2500)
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


def append_row_to_csv(file_path, row, columns=None):
    if columns == None:
        columns = list(row.keys())
    df = pd.DataFrame([row], columns=columns)
    file_exists = os.path.exists(file_path)
    if not file_exists:
        df.to_csv(file_path, header=True, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)


def divide_to_tables(data, rider_id):
    '''
    Divide data dictionary into relevant tables
    '''

    # workout
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
        if key in WORKOUTS_COLS:
            workout_row[key] = value
            found = True
        if key in WORKOUTS_HRS_COLS:
            workout_hrs_row[key] = value
            found = True
        if key in WORKOUTS_CADENCES_COLS:
            workout_cadences_row[key] = value
            found = True
        if key in WORKOUTS_POWERS_COLS:
            workout_powers_row[key] = value
            found = True
        if key in WORKOUTS_SPEEDS_COLS:
            workout_speeds_row[key] = value
            found = True
        if not found:
            key_not_found.append(key)

    for key in WORKOUTS_COLS:
        if key not in workout_row:
            workout_row[key] = None

    for key in WORKOUTS_HRS_COLS:
        if key not in workout_hrs_row:
            workout_hrs_row[key] = None

    for key in WORKOUTS_CADENCES_COLS:
        if key not in workout_cadences_row:
            workout_cadences_row[key] = None

    for key in WORKOUTS_POWERS_COLS:
        if key not in workout_powers_row:
            workout_powers_row[key] = None

    for key in WORKOUTS_SPEEDS_COLS:
        if key not in workout_speeds_row:
            workout_speeds_row[key] = None

    return workout_row, workout_hrs_row, workout_cadences_row, workout_powers_row, workout_speeds_row, key_not_found
