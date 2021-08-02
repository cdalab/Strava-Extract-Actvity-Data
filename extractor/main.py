import sys
sys.path.append('../')

import pickle as pk
import requests
from get_activities_data import Get_Activities_Data
from get_activities_links import Get_Activities_Links
from rider import Rider
from usernames import *


if __name__ == '__main__':

    ip = requests.get('http://ipinfo.io/json').json()['ip']

    activity_type = sys.argv[1]
    file_name = sys.argv[2]
    user_index = int(sys.argv[3])

    riders_pickle = open(f'data/{file_name}.pickle', 'rb')
    riders = pk.load(riders_pickle)

    if activity_type == 'data':

        # run example : main.py data ISN_riders 2 200 500
        print("---- START EXTRACTING DATA ----")

        riders_range_low = int(sys.argv[4])
        riders_range_high = int(sys.argv[5])

        data_extractor = Get_Activities_Data(usernames[user_index], riders[riders_range_low :riders_range_high], ip)
        data_extractor.run()

        # save ...
        with open(f'data/{file_name}_{riders_range_low}_{riders_range_high}.pickle', 'wb') as handle:
            pk.dump(data_extractor.riders, handle, protocol=pk.HIGHEST_PROTOCOL)



    elif activity_type == 'link':
        # run example : main.py link ISN_riders 2 2015 2021 1 12
        print("---- START EXTRACTING LINKS ----")

        extract_from_year = int(sys.argv[4])
        extract_to_year = int(sys.argv[5]) + 1
        extract_from_month = int(sys.argv[6])
        extract_to_month = int(sys.argv[7]) + 1

        links_extractor = Get_Activities_Links(usernames[user_index],
                                         list(range(extract_from_year, extract_to_year)),
                                         list(range(extract_from_month, extract_to_month)))

        links_extractor.create_links_for_extractions()
        links_extractor.run()

        with open(f'data/{file_name}_years_{extract_from_year}_{extract_to_year - 1}_months_{extract_from_month}_{extract_to_month - 1}.pickle', 'wb') as handle:
            pk.dump(links_extractor.riders, handle, protocol=pk.HIGHEST_PROTOCOL)

    print("---- FINISH ----")