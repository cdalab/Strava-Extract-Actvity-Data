
import requests

from firebase import *
from rider import Rider
from utils import *
from bs4 import BeautifulSoup
import pandas as pd
import time as t
import sys

LOGGED_OUT_SLEEP = 1801
LOGIN_URL = 'https://www.strava.com/login'
ONBOARD_URL = 'https://www.strava.com/onboarding'


class Fill_location():

    def __init__(self, file_name,start, end, id, save_file_name):
        self.file_name = file_name
        self.STRAVA_URL = 'https://www.strava.com'
        self.ACTIVITY_URL = 'https://www.strava.com/activities/'
        self.id = id
        self.curr_user = ''
        self.start = start
        self.end = end
        self.save_file_name = save_file_name

    def _check_if_too_many_requests(self, url_to_refresh):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        found = re.search('too many requests' ,str(soup).lower())
        if found is not None:
            # Too many requests
            log('Too many requests: SWITCHING ACCOUNT', 'ERROR', id=self.id)
            self._switchAccount(url_to_refresh)

    def _switchAccount(self, url_to_refresh):
        self._close_driver()
        self._open_driver()
        self.browser.get(url_to_refresh)
        t.sleep(0.5)

    def _get_username(self):
        rand_index = random.randint(0, len(usernames)-1)
        self.curr_user = usernames[rand_index]
        return usernames[rand_index]

    def _open_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        URL = self.STRAVA_URL + '/login'
        self.browser.get(URL)
        email = self.browser.find_element_by_id("email")
        password = self.browser.find_element_by_id("password")
        user = self._get_username()
        email.send_keys(user)
        password.send_keys('12345678')

        self.browser.find_element_by_id("login-button").click()
        t.sleep(1)

        if self.browser.current_url == LOGIN_URL:
            # ip blocked...

            log(f"IP BLOCKED - waiting for {LOGGED_OUT_SLEEP} seconds.", 'ERROR', id=self.id)
            self._close_driver()
            t.sleep(LOGGED_OUT_SLEEP)
            self._open_driver()
        elif not self.browser.current_url == 'https://www.strava.com/onboarding':
            # BAD ACCOUNT! need
            log(f"BAD ACCOUNT {user} {self.browser.current_url}: SWITCHING ACCOUNT", 'ERROR', id=self.id)

            self._close_driver()
            self._open_driver()
            t.sleep(300)

        else:
            log(f'LOGGED IN WITH {user}, {self.browser.current_url}', id=self.id)



    def _close_driver(self):
        self.browser.close()

    def _is_logged_out(self):
        try:
            site_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            if site_soup.find('html')['class'][0] == 'logged-out': # logged out ...
                log(f'logged out. username: {self.curr_user}', 'ERROR', id=self.id)

                return True

            return False
        except:
            return False # Failed to check if logged in....


    def fill(self):
        self._open_driver()
        self.df = pd.read_csv(self.file_name+'.csv')
        for index, row in self.df.iterrows():
            if index < self.start or index >= self.end:
                continue
            url = self.ACTIVITY_URL + str(row['workout_strava_id'])
            self.browser.get(url)
            t.sleep(0.5)
            self._check_if_too_many_requests(url)
            activity_soup = BeautifulSoup(self.browser.page_source, 'html.parser')

            timeout = t.time() + 3
            while True:
                t.sleep(0.5)
                try:
                    row['workout_location'] = activity_soup.find('span', {'class': 'location'}).text
                    append_row_to_csv(self.save_file_name, row, workout_columns)
                    log(f'{index} / {self.end-self.start} | {url} |', id=self.id)
                    break
                except Exception as e:
                    if t.time() > timeout:
                        row['workout_location'] = ''
                        append_row_to_csv(self.save_file_name, row, workout_columns)
                        log(f'Failed to find location | {url} | {e}','ERROR', id=self.id)
                        break
            

        self._close_driver()


start = int(sys.argv[1])
end = int(sys.argv[2])


save_file_name = f'fill/workout_fill_location_{start}_{end}'
id = requests.get('http://ipinfo.io/json').json()['ip'] + '_location'
fill_location = Fill_location('data/filltered_workouts',start, end, id, save_file_name)
fill_location.fill()

try:
    init_firebase()
    upload_data_firebase(save_file_name, str(fill_location.df.to_csv()))
    log(f'SAVED TO FIREEBAE', id=id)
except Exception as e:
    print(e)







