import sys
import pickle as pk
import requests
import pandas as pd
from get_activities_data import Get_Activities_Data
from get_activities_links import Get_Activities_Links
from usernames import *
from utils import valid_rider_url, log
from firebase import upload_data_firebase, init_firebase
from rider import Rider




def link(riders, extract_from_year, extract_to_year, extract_from_month, extract_to_month):

    print("---- START EXTRACTING ACTIVITY LINKS ----")
    links_extractor = Get_Activities_Links(riders,
                                           list(range(extract_from_year, extract_to_year)),
                                           list(range(extract_from_month, extract_to_month)))

    links_extractor.create_links_for_extractions()
    links_extractor.run()

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    return links_extractor.riders


def data(saving_file_name, riders, riders_range_low, riders_range_high, ip, start_from_index):

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Data(riders[riders_range_low:riders_range_high], id=ip, saving_file_name=saving_file_name, start_from_index=start_from_index)
    data_extractor.run()
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return data_extractor.riders


def flow(saving_file_name, csv_file, ip, team_ids=None, start_index=0, end_index= float('inf')):

    print("---- START CREATING LIST OF RIDERS ----")

    riders_pickle = open(f'data/ISN_riders.pickle', 'rb')
    isn_riders = pk.load(riders_pickle)
    isn_ids = [rider.rider_id for rider in isn_riders]

    df = pd.read_csv(f"data/{csv_file}.csv")
    df = df[df['url'].notna()]
    df = df[~df['cyclist_id'].isin(isn_ids)]
    print(len(df))
    riders = []

    i = 0
    for index, row in df.iterrows():

        if i >= start_index and i < end_index:
            try:
                rider_years = row['year'].split(',')
                rider = Rider(row['full_name'], row['url'], row['cyclist_id'], years=rider_years)
            except:
                #print('no years...')
                rider = Rider(row['full_name'], row['url'], row['cyclist_id'])


            try:
                rider_teams = row['team_pcs_id'].split(',')
            except:
                rider_teams = []
            if valid_rider_url(rider.rider_url) :
                if (team_ids is not None and len(list(set(rider_teams) & set(team_ids))) > 0) or team_ids is None :

                    riders.append(rider)
        i += 1

    print(f"---- FINISHED CREATION - THERE ARE {len(riders)} riders ----")

    print("---- START EXTRACTING ACTIVITY LINKS ----")

    links_extractor = Get_Activities_Links(riders, ip)
    links_extractor.create_links_for_extractions()

    links_extractor.run()
    riders = links_extractor.riders

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Data(riders, id=ip, saving_file_name=saving_file_name)
    data_extractor.run()
    riders = data_extractor.riders
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return riders



def save_csv(file_name, riders):

    if riders is None:
        print('No riders to save...')
        return
    workout, workout_hrs, workout_cadences, workout_powers, workout_speeds = [], [], [], [], []
    for rider in riders:
        r_workout, r_workout_hrs, r_workout_cadences, r_workout_powers, r_workout_speeds = rider.to_data()
        workout += r_workout
        workout_hrs += r_workout_hrs
        workout_cadences += r_workout_cadences
        workout_powers += r_workout_powers
        workout_speeds += r_workout_speeds

    table_names = ['workout', 'workout_hrs', 'workout_cadences', 'workout_powers', 'workout_speeds']
    tables = [workout, workout_hrs, workout_cadences, workout_powers, workout_speeds]

    # for i in range(len(tables)):
    #     new_file_name = f'{file_name}_{table_names[i]}.csv'
    #     pd.DataFrame(tables[i]).to_csv(new_file_name)

    try:
        init_firebase()
        for i in range(len(tables)):
            new_file_name = f'{file_name}_{table_names[i]}.csv'
            try:
                upload_data_firebase(new_file_name, str(pd.DataFrame(tables[i]).to_csv()))
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


if __name__ == '__main__':


    id = requests.get('http://ipinfo.io/json').json()['ip']

    activity_type = sys.argv[1]
    file_name = sys.argv[2]




    if activity_type == 'data':

        # run example : main.py data ISN_riders 200 500
        # run example : main.py data ISN_riders 200 500 -i 4

        riders_pickle = open(f'data/{file_name}.pickle', 'rb')
        riders_load = pk.load(riders_pickle)

        riders_range_low = int(sys.argv[3])
        riders_range_high = int(sys.argv[4])

        saving_file_name = f'data/{file_name}_{riders_range_low}_{riders_range_high}'
        index = False
        start_from_index = 0
        try:
            i = sys.argv[5]
            if (i == "-i"):
                start_from_index = int(sys.argv[6])
                saving_file_name += f'_started from: {start_from_index}'
        except Exception as e:
            print(e)

        data_riders = None

        try:
            data_riders = data(saving_file_name, riders_load, riders_range_low, riders_range_high, id, start_from_index)
        except Exception as e:
            print(e)

        save_csv(saving_file_name, data_riders)

    elif activity_type == 'link':
        # run example : main.py link ISN_riders 2015 2021 1 12

        riders_pickle = open(f'data/{file_name}.pickle', 'rb')
        riders_load = pk.load(riders_pickle)

        extract_from_year = int(sys.argv[3])
        extract_to_year = int(sys.argv[4]) + 1
        extract_from_month = int(sys.argv[5])
        extract_to_month = int(sys.argv[6]) + 1

        link_riders = link(riders_load, extract_from_year, extract_to_year, extract_from_month, extract_to_month)
        saving_file_name = f'data/{file_name}_years_{extract_from_year}_{extract_to_year - 1}_months_{extract_from_month}_{extract_to_month - 1}.pickle'

        with open(saving_file_name, 'wb') as handle:
            pk.dump(link_riders, handle, pk.HIGHEST_PROTOCOL)

    elif activity_type == 'flow':
        print("---- START FLOW ----")
        # run example: main.py flow rider_csv
        # run example: main.py flow rider_csv -i 100 153 164
        # run example: main.py flow rider_csv -r 10 20

        saving_file_name = ""
        flow_riders = []
        saving_folder = 'flow/'
        try:
            i = sys.argv[3]
            if i == "-i":
                team_ids = sys.argv[4:]
                team_ids = [int(team) for team in team_ids]
                if len(team_ids) == 0:
                    teams_ids = None

                saving_file_name = f'flow/{file_name}_team_id_{team_ids}'
                log(f'STARTING FLOW TEAM_IDS: {team_ids}', id=id)
                flow_riders = flow(saving_file_name, file_name, id, team_ids=team_ids)

            elif i == '-r':

                low_index = int(sys.argv[4])
                high_index = int(sys.argv[5])
                saving_file_name = f'flow/{file_name}_index_{low_index}_{high_index}'
                log(f'STARTING FLOW INDEX: {low_index}_{high_index}', id=id)
                flow_riders = flow(saving_file_name, file_name, id, start_index=low_index, end_index=high_index)


        except:
            log(f'STARTING FLOW ALL', id=id)
            saving_file_name = f'flow/{file_name}_all'
            flow_riders = flow(saving_file_name, file_name, id)

        save_csv(saving_file_name, flow_riders)

    elif activity_type == 'actv':

        print("---- START FETCH ACTIVITIES ----")
        # run example: main.py actv strava_ids 1 100
        # run example: main.py actv strava_ids

        riders_range_low = int(sys.argv[3])
        riders_range_high = int(sys.argv[4])

        df = pd.read_csv(f'data/{file_name}.csv')
        print(len(df))
        riders_dic = {}
        i = -1
        for index, row in df.iterrows():
            i += 1
            if i < riders_range_low or i >= riders_range_high:
                continue

            if row.cyclist_id not in riders_dic:
                riders_dic[row.cyclist_id] = Rider(rider_name='', rider_url='',rider_id=row.cyclist_id)
            url = f"https://www.strava.com/activities/{row.workout_strava_id}"
            riders_dic[row.cyclist_id].activity_links.add(url)



        saving_file_name = f'actv/{file_name}_{riders_range_low}_{riders_range_high}'

        data_riders = None
        try:
            riders = list(riders_dic.values())
            data_riders = data(saving_file_name, list(riders_dic.values()), 0, len(riders), id, 0)
        except Exception as e:
            print(e)

        save_csv(saving_file_name, data_riders)




    print("---- FINISH ----")
