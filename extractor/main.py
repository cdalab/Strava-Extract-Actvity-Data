import sys
import pickle as pk
import requests
import pandas as pd
from get_activities_data import Get_Activities_Data
from get_activities_links import Get_Activities_Links
from usernames import *
from utils import valid_rider_url
from firebase import upload_riders


def link(username, riders, extract_from_year, extract_to_year, extract_from_month, extract_to_month):

    print("---- START EXTRACTING ACTIVITY LINKS ----")
    links_extractor = Get_Activities_Links(username,
                                           riders,
                                           list(range(extract_from_year, extract_to_year)),
                                           list(range(extract_from_month, extract_to_month)))

    links_extractor.create_links_for_extractions()
    links_extractor.run()

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    return links_extractor.riders


def data(username, riders, riders_range_low, riders_range_high, ip):

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Data(username, riders[riders_range_low:riders_range_high], ip)
    data_extractor.run()
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return data_extractor.riders

def flow(username, csv_file, ip):
    print("---- START FLOW ----")
    print("---- START CREATING LIST OF RIDERS ----")
    df = pd.read_csv(f'data/{csv_file}.csv')
    df = df[df['url'].notna()]
    riders = []

    for index, row in df.iterrows():
        rider = Rider(row['full_name'], row['url'], row['cyclist_id'])
        if valid_rider_url(rider.rider_url):
            riders.append(rider)

    print(f"---- FINISHED CREATION - THERE ARE {len(riders)} riders ----")

    print("---- START EXTRACTING ACTIVITY LINKS ----")

    links_extractor = Get_Activities_Links(username, riders)
    links_extractor.create_links_for_extractions()
    links_extractor.run()
    riders = links_extractor.riders

    print("---- FINISHED EXTRACTING ACTIVITY LINKS ----")

    print("---- START EXTRACTING ACTIVITY DATA ----")
    data_extractor = Get_Activities_Data(username, riders, ip)
    data_extractor.run()
    riders = data_extractor.riders
    print("---- FINISHED EXTRACTING ACTIVITY DATA ----")
    return riders


if __name__ == '__main__':


    sys.path.append('../')
    from rider import Rider

    ip = requests.get('http://ipinfo.io/json').json()['ip']

    activity_type = sys.argv[1]
    file_name = sys.argv[2]
    user_index = int(sys.argv[3])

    riders_pickle = open(f'data/{file_name}.pickle', 'rb')
    riders_load = pk.load(riders_pickle)

    if activity_type == 'data':

        # run example : main.py data ISN_riders 2 200 500

        riders_range_low = int(sys.argv[4])
        riders_range_high = int(sys.argv[5])

        data_riders = data(usernames[user_index], riders_load, riders_range_low, riders_range_high, ip)
        saving_file_name = f'data/{file_name}_{riders_range_low}_{riders_range_high}'

        # save ...
        upload_riders(saving_file_name, data_riders)

        # with open(saving_file_name, 'wb') as handle:
        #     pk.dump(data_riders, handle, protocol=pk.HIGHEST_PROTOCOL)

    elif activity_type == 'link':
        # run example : main.py link ISN_riders 2 2015 2021 1 12


        extract_from_year = int(sys.argv[4])
        extract_to_year = int(sys.argv[5]) + 1
        extract_from_month = int(sys.argv[6])
        extract_to_month = int(sys.argv[7]) + 1

        link_riders = link(usernames[user_index], riders_load, extract_from_year, extract_to_year, extract_from_month, extract_to_month)
        saving_file_name = f'data/{file_name}_years_{extract_from_year}_{extract_to_year - 1}_months_{extract_from_month}_{extract_to_month - 1}.pickle'

        with open(saving_file_name, 'wb') as handle:
            pk.dump(link_riders, handle, pk.HIGHEST_PROTOCOL)
    elif activity_type == 'flow':

        # run example: main.py flow rider_csv
        flow_riders = flow(usernames[user_index], file_name, ip)
        saving_file_name = f'data/{file_name}_{flow}.pickle'
        with open(saving_file_name, 'wb') as handle:
            pk.dump(flow_riders, handle, pk.HIGHEST_PROTOCOL)



    print("---- FINISH ----")