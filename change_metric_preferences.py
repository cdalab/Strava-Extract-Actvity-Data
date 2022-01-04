import time as t
import traceback
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from browser import Browser
from bs4 import BeautifulSoup
from utils import log
from usernames import usernames
import random
from selenium.webdriver.common.keys import Keys

BASE_URL = 'https://www.strava.com/'
LOGGED_OUT_SLEEP = 1801
LOGIN_URL = 'https://www.strava.com/login'
ONBOARD_URL = 'https://www.strava.com/onboarding'
DASHBOARD_URL = 'https://www.strava.com/dashboard'

class Change_Metric_Preferences(Browser):

    def __init__(self, id, start_user=None):
        '''
        data : Dictionary<RIDER_ID, Activity_ID>
        Example: {1: 6418596161}
        '''

        super().__init__(id)
        self.start_user = start_user

    def start(self):
        for user in usernames:
            '''
            Main method. Opens a new driver. Then tries to login to strava
            '''
            if (self.start_user is not None) and self.start_user != user:
                continue
            if self.start_user is not None:
                self.start_user = None
                continue
            preferences = {"download.default_directory": 'downloads/', "directory_upgrade": True,
                           "safebrowsing.enabled": True}
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('--no-sandbox')
            options.add_argument("download.default_directory=Downloads/")
            options.add_experimental_option("prefs", preferences)
            self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

            URL = self.STRAVA_URL + '/login'
            self.browser.get(URL)
            email = self.browser.find_element_by_id("email")  # Get email element
            password = self.browser.find_element_by_id("password")  # Get password element
            # user = self._get_username()
            email.send_keys(user)  # send email with our username
            password.send_keys('12345678')  # send our default password 12345678

            self.browser.find_element_by_id("login-button").click()  # press the login button
            t.sleep(random.random() + random.randint(0,6))

            if self.browser.current_url == LOGIN_URL:
                # ip blocked... wait until block is removed
                log(f"IP BLOCKED", 'WARNING', id=self.id)
                self.browser.close()
                t.sleep(LOGGED_OUT_SLEEP)
                self.start_user = user
                self.start()
                return

            elif not self.browser.current_url == ONBOARD_URL and not self.browser.current_url == DASHBOARD_URL:
                # BAD ACCOUNT! need
                log(f"BAD ACCOUNT {user} {self.browser.current_url}", 'WARNING', id=self.id)
                self.browser.close()
                t.sleep(LOGGED_OUT_SLEEP/5)
                self.start_user = user
                self.start()
                return

            else:
                # Success! we are logged in
                log(f'LOGGED IN WITH {user}, {self.browser.current_url}', id=self.id)
                self.browser.get('https://www.strava.com/settings/display')
                try:

                    preferences_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    preferences = preferences_soup.find_all('div', attrs={'class': "setting-value"})
                    TIMEOUT = 5
                    trials = 0
                    while 'Kilometers and Kilograms' not in preferences[0].get_text():
                        # MILES & POUNDS -> KGs & KMs
                        self.browser.find_elements_by_css_selector(
                            'div[class="app-icon icon-dark icon-edit icon-sm"]')[0].click()  # CLICK TO EDIT
                        t.sleep(random.random() + random.randint(0,6))
                        self.browser.find_element_by_xpath(
                            "//select[@id='default-measurement-js']/option[text()='Kilometers and Kilograms']").click()  # SELECT METRIC
                        t.sleep(random.random() + random.randint(0,6))
                        self.browser.find_element_by_id('contents').find_elements_by_class_name('btn-sm')[0].click()  # SAVE
                        t.sleep(random.random() + random.randint(2,6))
                        trials+=1
                        if trials > TIMEOUT:
                            raise TimeoutError('cannot change preference: MILES & POUNDS -> KGs & KMs')
                        preferences_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                        preferences = preferences_soup.find_all('div', attrs={'class': "setting-value"})

                    trials = 0
                    while 'Celsius' not in preferences[1].get_text():
                        # Fahrenheit -> Celsius
                        self.browser.find_elements_by_css_selector(
                            'div[class="app-icon icon-dark icon-edit icon-sm"]')[1].click()  # CLICK TO EDIT
                        t.sleep(random.random() + random.randint(0,6))
                        self.browser.find_element_by_xpath(
                            "//select[@id='temperature-measurement-js']/option[text()='Celsius']").click()  # SELECT METRIC
                        t.sleep(random.random() + random.randint(1,6))
                        # save_trials = 0
                        # while save_trials < TIMEOUT:
                            # try:
                        self.browser.find_element_by_id('contents').find_element_by_id(
                                'submit-button').send_keys(Keys.ENTER)
                                # self.browser.find_element_by_xpath(
                                #     '/html/body/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/form').submit()
                                # self.browser.switch_to.active_element
                                # self.browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[1]/div[1]/div[2]/div/form/div[3]/button').click()
                                # self.browser.find_element_by_id('contents').find_element_by_id('submit-button').click() # SAVE
                        #         break
                        #     except Exception as err:
                        #         if 'no such element' in str(err):
                        #             break
                        #         save_trials += 1
                        #         t.sleep(random.random() + random.randint(0, 6))
                        #         raise err
                        # if save_trials >= TIMEOUT:
                        #     raise TimeoutError('cannot change preference: Fahrenheit -> Celsius')
                        t.sleep(random.random() + random.randint(0,6))
                        trials += 1
                        if trials > TIMEOUT:
                            raise TimeoutError('cannot change preference: Fahrenheit -> Celsius')
                        preferences_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                        preferences = preferences_soup.find_all('div', attrs={'class': "setting-value"})

                    log(f'{user}', 'Info', id='verification')

                except:
                    log(f'FAILED! {user}, {self.browser.current_url}, ERROR DETAILS: {traceback.format_exc()} ', id=self.id)


class Validate_Metric_Preferences(Browser):

    def __init__(self, id, start_user=None):
        '''
        data : Dictionary<RIDER_ID, Activity_ID>
        Example: {1: 6418596161}
        '''

        super().__init__(id)
        self.start_user = start_user

    def start(self):
        for user in usernames:
            try:
                if (self.start_user is not None) and self.start_user != user:
                    continue
                self.start_user = None

                '''
                Main method. Opens a new driver. Then tries to login to strava
                '''

                preferences = {"download.default_directory": 'downloads/', "directory_upgrade": True,
                               "safebrowsing.enabled": True}
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('--no-sandbox')
                options.add_argument("download.default_directory=Downloads/")
                options.add_experimental_option("prefs", preferences)
                self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

                URL = self.STRAVA_URL + '/login'
                self.browser.get(URL)
                email = self.browser.find_element_by_id("email")  # Get email element
                password = self.browser.find_element_by_id("password")  # Get password element
                # user = self._get_username()
                email.send_keys(user)  # send email with our username
                password.send_keys('12345678')  # send our default password 12345678

                self.browser.find_element_by_id("login-button").click()  # press the login button
                t.sleep(random.random() + random.randint(0,6))

                if self.browser.current_url == LOGIN_URL:
                    # ip blocked... wait until block is removed
                    log(f"IP BLOCKED", 'WARNING', id='metric_valid')
                    self.browser.close()
                    t.sleep(LOGGED_OUT_SLEEP)
                    self.start_user = user
                    self.start()
                    log(f"TEST3 {user}", 'WARNING', id='test')
                    return

                elif not self.browser.current_url == ONBOARD_URL and not self.browser.current_url == DASHBOARD_URL:
                    # BAD ACCOUNT! need
                    log(f"BAD ACCOUNT {user} {self.browser.current_url}", 'WARNING', id=self.id)
                    self.browser.close()
                    t.sleep(LOGGED_OUT_SLEEP/5)
                    self.start_user = user
                    self.start()
                    log(f"TEST4 {user}", 'WARNING', id='test')
                    return
                else:
                    # Success! we are logged in
                    log(f'LOGGED IN WITH {user}, {self.browser.current_url}', id=self.id)
                    self.browser.get('https://www.strava.com/settings/display')

                    preferences_soup = BeautifulSoup(self.browser.page_source, 'html.parser')

                    preferences = preferences_soup.find_all('div',attrs={'class':"setting-value"})
                    # confirm metrics: KGs & KMs
                    if 'Kilometers and Kilograms' not in preferences[0].get_text():
                        log(f"WRONG METRICS (KGs & KMs) - {user}", 'WARNING', id='metric')
                        continue

                    # confirm metrics: Celsius
                    if 'Celsius' not in preferences[1].get_text():
                        log(f"WRONG METRICS (Celsius) - {user}", 'WARNING', id='metric')
                        continue

                    log(f'{user}','Info',id='verification')
            except:
                log(f'Error! {traceback.format_exc()}', 'Info', id='verification')
