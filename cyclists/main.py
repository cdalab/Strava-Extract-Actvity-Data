import sys
import pickle as pk
import requests
from extract_activity_data import Activities_Extractor
from rider import Rider

password = r'1357WorkWork!'
password_cool_tables = '1357Worker!'
usernames = [
    r'kvspek@gmail.com',
    r'spektork@post.bgu.ac.il',
    r'kev_backup@yahoo.com',
    r'cool_table@yahoo.com',
    r'cool_table2@yahoo.com',
    r'cool_table3@yahoo.com',
    r'cool_table4@yahoo.com',
    r'cool_table5@yahoo.com',
    r'cool_table6@yahoo.com',
    r'cool_table7@yahoo.com',
    r'cool_table8@yahoo.com'
]

username_backup = r'kev_backup@yahoo.com'
password_backup = r'1357Backup!'


if __name__ == '__main__':

    # run example : main.py 2 200 500

    ip = requests.get('http://ipinfo.io/json').json()['ip']

    print("---- START ----")
    riders_pickle = open('data/ISN_riders.pickle', 'rb')
    riders = pk.load(riders_pickle)

    user_index = int(sys.argv[1])
    riders_range_low = int(sys.argv[2])
    riders_range_high = int(sys.argv[3])

    extractor = Activities_Extractor(usernames[user_index], riders[riders_range_low:riders_range_high], ip)
    extractor.run()
    # for w in extractor.riders[0].workout:
    #     print(w)

    # save ...
    with open(f'data/ISN_riders_{riders_range_low}_{riders_range_high}.pickle', 'wb') as handle:
        pk.dump(extractor.riders, handle, protocol=pk.HIGHEST_PROTOCOL)

    print("---- FINISH ----")
