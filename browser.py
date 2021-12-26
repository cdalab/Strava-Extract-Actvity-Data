
from usernames import *
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time as t
from utils import log
import re




MIN_RAND_SLEEP = 5
MAX_RAND_SLEEP = 20
LOGGED_OUT_SLEEP = 1801
LOGIN_URL = 'https://www.strava.com/login'
ONBOARD_URL = 'https://www.strava.com/onboarding'
DASHBOARD_URL = 'https://www.strava.com/dashboard'



class Browser:
    def __init__(self, id):
        self.id = id
        self.STRAVA_URL = 'https://www.strava.com'
        self.curr_user = ''
        
    def _check_if_too_many_requests(self, url_to_refresh):
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        found = re.search('too many requests' ,str(soup).lower())
        while found is not None:
            # Too many requests
            log(f'Too many requests: {self.curr_user} SWITCHING ACCOUNT', 'ERROR', id=self.id)
            self._switchAccount(url_to_refresh)
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            found = re.search('too many requests' ,str(soup).lower())
            t.sleep(0.5)

    def _switchAccount(self, url_to_refresh):
        self._close_driver()
        self._open_driver()
        self.browser.get(url_to_refresh)
        t.sleep(0.5)

    def _restart_browser(self):
        self._open_driver()
        t.sleep(0.5)

    def _get_username(self):
        rand_index = random.randint(0, len(usernames)-1)
        self.curr_user = usernames[rand_index]
        return usernames[rand_index]

    def _open_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        
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

            log(f"IP BLOCKED - waiting for {LOGGED_OUT_SLEEP} seconds.", 'WARNING', id=self.id)
            self._close_driver()
            t.sleep(LOGGED_OUT_SLEEP)
            self._open_driver()
        elif not self.browser.current_url == ONBOARD_URL and not self.browser.current_url == DASHBOARD_URL:
            # BAD ACCOUNT! need
            log(f"BAD ACCOUNT {user} {self.browser.current_url}: SWITCHING ACCOUNT", 'WARNING', id=self.id)

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

