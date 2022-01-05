import sys
import pickle as pk
from pathlib import Path

import pandas as pd
from get_activities_info import Get_Activities_Info
from get_activities_links import Get_Activities_Links
from get_activities_html import Get_Activities_HTML
from utils import valid_rider_url, log, setting_up

def extract_rider_links(urls_file_path, id,csv_file_path='link/rider_links_results.csv', low_limit_index=0, high_limit_index=None):
    log("---- START EXTRACTING RIDER LINKS ----",id=id)

    riders_df = pd.read_csv(f"{urls_file_path}")
    riders_df = riders_df[riders_df['strava_link'].notna()]
    if high_limit_index:
        riders_df = riders_df.loc[low_limit_index:high_limit_index-1]
    else:
        riders_df = riders_df.loc[low_limit_index:]
    links_extractor = Get_Activities_Links(riders=riders_df,
                                           id=id,
                                           csv_file_path=csv_file_path)
    links_extractor.fetch_rider_links()


    log("---- FINISHED EXTRACTING RIDER LINKS ----",id=id)

def extract_rider_activities_links(links_file_path, id, csv_file_path='link/riders_time_interval_pages', low_limit_index=0, high_limit_index=None):
    log("---- START EXTRACTING TIME INTERVAL LINKS ----",id=id)

    riders_links_df = pd.read_csv(f"{links_file_path}")
    non_nan_pred = ~((riders_links_df['first_link'].isna()) & (riders_links_df['options'].isna()))
    riders_links_df = riders_links_df.loc[non_nan_pred]
    if high_limit_index:
        riders_links_df = riders_links_df.loc[low_limit_index:high_limit_index-1]
    else:
        riders_links_df = riders_links_df.loc[low_limit_index:]
    links_extractor = Get_Activities_Links(riders=riders_links_df,
                                           id=id,
                                           csv_file_path=csv_file_path)
    links_extractor.fetch_rider_time_interval_links()


    log("---- FINISHED EXTRACTING TIME INTERVAL LINKS ----",id=id)


def info(file_path, riders, id, start_from_index):
    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Info(riders, id=id,
                                         file_path=file_path, start_from_index=start_from_index)
    data_extractor.run()
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return data_extractor.riders


def flow(saving_file_name, csv_file, ip, team_ids=None, start_index=0, end_index=float('inf')):
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
                rider = Rider(row['url'], row['cyclist_id'], years=rider_years)
            except:
                # print('no years...')
                rider = Rider(row['url'], row['cyclist_id'])

            try:
                rider_teams = row['team_pcs_id'].split(',')
            except:
                rider_teams = []
            if valid_rider_url(rider.rider_url):
                if (team_ids is not None and len(list(set(rider_teams) & set(team_ids))) > 0) or team_ids is None:
                    riders.append(rider)
        i += 1

    print(f"---- FINISHED CREATION - THERE ARE {len(riders)} riders ----")

    print("---- START EXTRACTING ACTIVITY LINKS ----")

    links_extractor = Get_Activities_Links(riders=riders, id=ip, saving_file_name=f"link{saving_file_name}")
    links_extractor.create_links_for_extractions()

    links_extractor.fetch_links()
    riders = links_extractor.riders

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Info(riders, id=ip, saving_file_name=f"flow/{saving_file_name}")
    data_extractor.run()
    riders = data_extractor.riders
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return riders


if __name__ == '__main__':

    args = setting_up()
    command = args['command']
    id = args['id']

    if command == 'info':

        # run example : main.py -c info -f ISN_pickle_riders.pickle -li 200 -hi 500
        # run example : main.py -c info -f ISN_pickle_riders.pickle -li 200 -hi 500 -l 4

        file_path = args['file_path']
        riders = pk.load(open(f'info/{file_path}', 'rb'))

        riders_low_index = args['riders_low_index']
        riders_high_index = args['riders_high_index']

        csv_file_path = f'{command}_{riders_low_index}_{riders_high_index}'
        start_from_index = args['low_limit_index']

        data_riders = None

        try:
            data_riders = info(csv_file_path, riders[riders_low_index:riders_high_index], id, start_from_index)
        except:
            log(f'Problem in info function, '
                f'args: {csv_file_path, riders[riders_low_index:riders_high_index], id, start_from_index}',
                'ERROR', id=id)



    elif command == 'extract_rider_links':
        # run example : main.py -c extract_rider_links -f data/ISN_riders.csv -t 2
        # run example : main.py -c extract_rider_links -f data/ISN_riders.csv -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        urls_file_path = args['file_path']
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        csv_file_path = f'link/rider_page_links'
        if low_limit_index:
            csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        if high_limit_index:
            csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path}.csv'
        Path("link/links").mkdir(parents=True, exist_ok=True)
        try:
            if low_limit_index:
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_links(urls_file_path, id, csv_file_path=csv_file_path, low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_rider_links(urls_file_path, id, csv_file_path=csv_file_path)

        except:
            log(f'Problem in extract_rider_links function, '
                f'args: {urls_file_path, id, csv_file_path, low_limit_index, high_limit_index}',
                'ERROR', id=id)

    elif command == 'extract_rider_time_interval_links':
        # run example : main.py -c extract_rider_time_interval_links -f link/rider_page_links.csv -t 2
        # run example : main.py -c extract_rider_time_interval_links -f link/rider_page_links.csv -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        links_file_path = args['file_path']
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        csv_file_path = f'link/riders_time_interval_links'
        if low_limit_index:
            csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        if high_limit_index:
            csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path}.csv'
        Path("link/riders_time_interval_pages").mkdir(parents=True, exist_ok=True)
        try:
            if low_limit_index:
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_activities_links(links_file_path, id, csv_file_path=csv_file_path, low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_rider_activities_links(links_file_path, id, csv_file_path=csv_file_path)

        except:
            log(f'Problem in extract_rider_links function, '
                f'args: {links_file_path, id, csv_file_path, low_limit_index, high_limit_index}',
                'ERROR', id=id)


    elif command == 'flow':
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

                saving_file_name = f'{file_name}_team_id_{team_ids}'
                log(f'STARTING FLOW TEAM_IDS: {team_ids}', id=id)
                flow_riders = flow(saving_file_name, file_name, id, team_ids=team_ids)

            elif i == '-r':

                low_index = int(sys.argv[4])
                high_index = int(sys.argv[5])
                saving_file_name = f'{file_name}_index_{low_index}_{high_index}'
                log(f'STARTING FLOW INDEX: {low_index}_{high_index}', id=id)
                flow_riders = flow(saving_file_name, file_name, id, start_index=low_index, end_index=high_index)


        except:
            log(f'STARTING FLOW ALL', id=id)
            saving_file_name = f'{file_name}_all'
            flow_riders = flow(saving_file_name, file_name, id)


    elif command == 'actv':

        print("---- START FETCH ACTIVITIES ----")
        # run example: main.py actv strava_ids 1 100
        # run example: main.py actc strava_ids 1 100 -i 20

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
                riders_dic[row.cyclist_id] = Rider(rider_name='', rider_url='', rider_id=row.cyclist_id)

            if row.workout_strava_id.isdecimal():
                url = f"https://www.strava.com/activities/{row.workout_strava_id}"
            else:
                url = row.workout_strava_id
            riders_dic[row.cyclist_id].activity_links.add(url)

        data_riders = None
        riders = list(riders_dic.values())
        saving_file_name = f'actv/{file_name}_{riders_range_low}_{riders_range_high}'
        try:

            try:
                i = sys.argv[5]
                if i == '-i':
                    start_from_index = int(sys.argv[6])
                    data_riders = data(saving_file_name, list(riders_dic.values()), 0, len(riders), id,
                                       start_from_index=start_from_index)
            except:
                data_riders = data(saving_file_name, list(riders_dic.values()), 0, len(riders), id, 0)
        except Exception as e:
            print(e)



    elif command == 'html':
        # run example: main.py html strava_ids 1 100
        # run example: main.py html strava_ids 1 100 -i 20

        links_range_low = int(sys.argv[3])
        links_range_low = int(sys.argv[4])
        start_from_index = 0
        try:
            i = sys.argv[5]
            if i == '-i':
                start_from_index = int(sys.argv[6])
        except:
            pass

        df = pd.read_csv(f'data/{file_name}.csv')
        data = []
        i = -1
        for index, row in df.iterrows():
            i += 1
            if i < links_range_low or i >= links_range_low:
                continue
            rider_id = row["rider_id"]
            activity_id = row["activity_id"]
            data.append((rider_id, activity_id))

        data = data[start_from_index:]

        Get_Activities_HTML(id, data)

    log("---- FINISH ----", id=id)
