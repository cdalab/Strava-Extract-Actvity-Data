
from consts import *
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
    '''
    Parent class for fetching data from strava
    '''
    
    
    def __init__(self, id):
        self.id = id
        self.STRAVA_URL = 'https://www.strava.com'
        self.curr_user = ''
        
    def _check_if_too_many_requests(self):
        '''
        Check if the the user account blocked - Too many request string returned.
        if blocked - switch to another user.
        '''
        
        
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        is_user_blocked = re.search('too many requests' ,str(soup).lower())
        if is_user_blocked is not None:
            log(f'Too many requests: {self.curr_user} SWITCHING ACCOUNT', 'ERROR', id=self.id)
            self._switchAccount()

    def _switchAccount(self):
        '''
        Restart browser -> close browser and reopen
        Then enter the url_to_refresh again
        '''
        self._close_driver()
        self._open_driver()

    def _restart_browser(self):
        '''
        Open the driver if something went wrong
        '''
        self._open_driver()
        t.sleep(0.5)

    def _get_username(self):
        '''
        Get a random username from the usernames pool
        '''
        rand_index = random.randint(0, len(USERS) - 1)
        self.curr_user = USERS[rand_index]
        return USERS[rand_index]

    def _open_driver(self):
        '''
        Main method. Opens a new driver. Then tries to login to strava
        '''

        preferences = {"download.default_directory": 'downloads/' , "directory_upgrade": True, "safebrowsing.enabled": True }
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('log-level=1')
        options.add_argument("download.default_directory=Downloads/")
        options.add_experimental_option("prefs", preferences)
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        URL = self.STRAVA_URL + '/login'
        self.browser.get(URL)
        email = self.browser.find_element_by_id("email") # Get email element
        password = self.browser.find_element_by_id("password") # Get password element
        user = self._get_username()
        email.send_keys(user) # send email with our username
        password.send_keys(PASSWORD) # send our default password 12345678

        self.browser.find_element_by_id("login-button").click() # press the login button
        t.sleep(random.random())

        if self.browser.current_url == LOGIN_URL:
            # ip blocked... wait until block is removed

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
            # Success! we are logged in
            log(f'LOGGED IN WITH {user}, {self.browser.current_url}', id=self.id)
            return self.browser, user



    def _close_driver(self):
        # Close driver with the close method
        self.browser.close()

    def _is_logged_out(self):
        '''
        Check if user is logged in.
        returns bool
        '''
        try:
            site_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            if site_soup.find('html')['class'][0] == 'logged-out': # logged out ...
                log(f'logged out. username: {self.curr_user}', 'ERROR', id=self.id)

                return True

            return False
        except:
            return False # Failed to check if logged in....

