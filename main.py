import sys
import pickle as pk
import requests
import pandas as pd
from get_activities_data import Get_Activities_Data
from get_activities_links import Get_Activities_Links
from get_activities_html import Get_Activities_HTML
from usernames import *
from utils import valid_rider_url, log
from firebase import upload_data_firebase, init_firebase
from rider import Rider
from pathlib import Path





def link(csv_file, id, saving_file_name, start_index=0, end_index= float('inf'), parallelism=1):

    print("---- START EXTRACTING ACTIVITY LINKS ----")

    df = pd.read_csv(f"data/{csv_file}.csv")
    df = df[df['url'].notna()]
    riders = []

    i = 0
    for index, row in df.iterrows():

        if i >= start_index and i < end_index:
            try:
                rider_years = row['year'].split(',')
                rider = Rider(row['url'], row['cyclist_id'], years=rider_years)
            except:
                #print('no years...')
                rider = Rider(row['url'], row['cyclist_id'])

            if valid_rider_url(rider.rider_url) :
                riders.append(rider)
        i += 1


    step = len(riders)//parallelism
    extractors = []
    for i in range(parallelism+1):
        curr = i*step
        if not len(riders) <= curr:
            links_extractor = Get_Activities_Links(riders=riders[curr:curr+step],
                                                id=id,
                                                saving_file_name = f'{saving_file_name}_{curr}_{curr+step}')

            extractors.append(links_extractor)
            links_extractor.start()
    for extractor in extractors:
        extractor.join()
        

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")
    riders = []
    for extractor in extractors:
        riders += extractor.riders


    return riders


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
                rider = Rider(row['url'], row['cyclist_id'], years=rider_years)
            except:
                #print('no years...')
                rider = Rider(row['url'], row['cyclist_id'])


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

    links_extractor = Get_Activities_Links(riders=riders, id=ip,saving_file_name=f"link/{saving_file_name}")
    links_extractor.create_links_for_extractions()

    links_extractor.fetch_links()
    riders = links_extractor.riders

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Data(riders, id=ip, saving_file_name=f"flow/{saving_file_name}")
    data_extractor.run()
    riders = data_extractor.riders
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return riders









if __name__ == '__main__':


    id = requests.get('http://ipinfo.io/json').json()['ip']


    log(f'', id=id)
    log(f'', id=id)
    log(f'====================================================================', id=id)
    log(f'{sys.argv}', id=id)
    log(f'', id=id)
    log(f'', id=id)
    activity_type = sys.argv[1]
    file_name = sys.argv[2]




    if activity_type == 'info':

        # run example : main.py info ISN_riders 200 500
        # run example : main.py info ISN_riders 200 500 -i 4

        riders_pickle = open(f'info/{file_name}.pickle', 'rb')
        riders_load = pk.load(riders_pickle)

        riders_range_low = int(sys.argv[3])
        riders_range_high = int(sys.argv[4])

        saving_file_name = f'info/{file_name}_{riders_range_low}_{riders_range_high}'
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

        

    elif activity_type == 'link':
        # run example : main.py link ISN_riders 1
        # run example : main.py link ISN_riders 1 -i 10 100

        parallelism = int(sys.argv[3])

        try:
            i = sys.argv[4]
            if i == "-i":
                low_index = int(sys.argv[5])
                high_index = int(sys.argv[6])
                saving_file_name = f'link/links_{file_name}_index_{low_index}_{high_index}'
                log(f'STARTING LINK INDEX: {low_index}_{high_index}', id=id)
                link(file_name, id, saving_file_name=saving_file_name, start_index=low_index, end_index=high_index, parallelism=parallelism)


        except:
            log(f'STARTING LINK ALL', id=id)
            saving_file_name = f'link/links_{file_name}_all'
            link(file_name, id, saving_file_name=file_name, parallelism=parallelism)

        


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

        save_csv(saving_file_name, flow_riders)

    elif activity_type == 'actv':

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
                riders_dic[row.cyclist_id] = Rider(rider_name='', rider_url='',rider_id=row.cyclist_id)
                
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
                    start_from_index =  int(sys.argv[6])
                    data_riders = data(saving_file_name, list(riders_dic.values()), 0, len(riders), id, start_from_index=start_from_index)
            except:
                data_riders = data(saving_file_name, list(riders_dic.values()), 0, len(riders), id, 0)
        except Exception as e:
            print(e)

        save_csv(saving_file_name, data_riders)
        
    
    elif activity_type == 'html':
        # run example: main.py html strava_ids 1 100
        # run example: main.py html strava_ids 1 100 -i 20
        
        
        links_range_low = int(sys.argv[3])
        links_range_low = int(sys.argv[4])
        start_from_index = 0
        try: 
            i = sys.argv[5]
            if i == '-i':
                start_from_index = int(sys.argv[6])
        except: pass
            

        df = pd.read_csv(f'data/{file_name}.csv')
        data = []
        i = -1
        for index, row in df.iterrows():
            i += 1
            if i < links_range_low or i >= links_range_low:
                continue
            rider_id = row["rider_id"]
            activity_id = row["activity_id"]
            data.append((rider_id,activity_id))
            
        data = data[start_from_index:]
            
        Get_Activities_HTML(id, data)

        
        
        
        




    print("---- FINISH ----")
