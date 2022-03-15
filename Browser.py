from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from consts import *
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time as t
from utils import log, timeout_wrapper
from itertools import cycle
import re


class Browser:
    '''
    Parent class for fetching data from strava
    '''

    def __init__(self, id, users=USERS):
        self.id = id
        self.curr_user = None
        self.user_pool = cycle(users)

    @timeout_wrapper
    def validate_units(self):
        self.browser.get(BASE_STRAVA_URL + '/settings/display')
        response = self._is_valid_html()
        if response is not None:
            raise ValueError(f'Display settings page is not loaded currectly, error {response}')
        settings = WebDriverWait(self.browser, 2).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "setting-value")))
        # validate metrics: KGs & KMs
        if 'Kilometers and Kilograms' not in settings[0].text:
            log(f"WRONG METRICS (Kilometers and Kilograms) - {self.curr_user}", 'WARNING', id=self.id)
            WebDriverWait(settings[0], 2).until(
                EC.presence_of_element_located((By.XPATH, "div"))).click()  # CLICK ON EDIT
            metric_selection_xpath = "//select[@id='default-measurement-js']/option[text()='Kilometers and Kilograms']"
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.XPATH, metric_selection_xpath))).click()  # SELECT METRIC
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.ID, 'submit-button'))).send_keys(Keys.ENTER) # SAVE
            raise ValueError(f"WRONG METRICS (KGs & KMs) - {self.curr_user}")

        # validate metrics: Celsius
        if 'Celsius' not in settings[1].text:
            log(f"WRONG METRICS (Celsius) - {self.curr_user}", 'WARNING', id=self.id)
            WebDriverWait(settings[1], 2).until(
                EC.presence_of_element_located((By.XPATH, "div"))).click()  # CLICK ON EDIT
            metric_selection_xpath = "//select[@id='temperature-measurement-js']/option[text()='Celsius']"
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.XPATH, metric_selection_xpath))).click()  # SELECT METRIC
            WebDriverWait(self.browser, 2).until(
                EC.presence_of_element_located((By.ID, 'submit-button'))).send_keys(Keys.ENTER) # SAVE
            raise ValueError(f"WRONG METRICS (Celsius) - {self.curr_user}")


    def browser_error_log_validation(self):
        for err in self.browser.get_log('browser'):
            if err['source'] == 'network':
                err_url = err['message'].split(' - ')[0]
                if '429' in err['message'].replace(err_url,''):
                    if 'strava' in err_url:
                        self.browser.get(err_url)
                        break

    def too_many_requests_loop(self, current_url):
        while True:
            log(f'Too many requests: {self.curr_user} SWITCHING ACCOUNT', 'WARNING', id=self.id)
            self._switch_account(current_url)
            self.browser_error_log_validation()
            WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
            soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            too_many_requests_error = re.search('too many requests', str(soup).lower())
            if too_many_requests_error is None:
                self.browser.get(current_url)
                break



    def _is_valid_html(self):
        current_url = self.browser.current_url
        self.browser_error_log_validation()
        WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        too_many_requests_error = re.search('too many requests', str(soup).lower())
        if too_many_requests_error is not None:
            self.too_many_requests_loop(current_url)
            return
        error_404 = soup.find(lambda tag: (tag.name == "div") and ('id' in tag.attrs) and ("error404" in tag['id']))
        if error_404 is not None:
            log(f"Page doesn't exist, url {current_url}", "WARNING", id=self.id)
            return 'error404'
        error_500 = soup.find(lambda tag: (tag.name == "div") and ('id' in tag.attrs) and ("error500" in tag['id']))
        if error_500 is not None:
            log(f"Page is not available, url {current_url}", "WARNING", id=self.id)
            return 'error_500'
        error_unknown = soup.find(lambda tag: (tag.name == "div") and ('id' in tag.attrs) and ("error" in tag['id']))
        if error_unknown is not None:
            log(f"Unknown Error in page, url {current_url}", "WARNING", id=self.id)
            return 'error_unknown'

    def _switch_account(self,url_last_session):
        '''
        Switch logged-in user
        '''
        self._close_driver()
        self._open_driver()
        self.browser.get(url_last_session)

    def _get_username(self):
        '''
        Get a username from the usernames pool
        '''
        self.curr_user = next(self.user_pool)
        return self.curr_user



    def _open_driver(self):
        '''
        Initialize selenium driver, then tries to login to STRAVA
        '''

        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('log-level=1')
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        self.browser.get(LOGIN_URL)
        email = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "email")))
        password = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "password")))
        user = self._get_username()
        email.send_keys(user)
        password.send_keys(PASSWORD)
        WebDriverWait(self.browser, 2).until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
        current_url = self.browser.current_url
        if current_url == LOGIN_URL:
            log(f"IP BLOCKED - waiting for {LOGGED_OUT_SLEEP} seconds.", 'WARNING', id=self.id)
            self._close_driver()
            t.sleep(LOGGED_OUT_SLEEP)
            self._open_driver()

        elif (not current_url == ONBOARD_URL) and (not current_url == DASHBOARD_URL):
            log(f"BAD ACCOUNT {user} {current_url}: SWITCHING ACCOUNT", 'WARNING', id=self.id)
            self._close_driver()
            self._open_driver()

        else:
            log(f'LOGGED IN WITH {user}, {self.browser.current_url}', id=self.id)
            return self.browser, user

    def _close_driver(self):
        self.browser.close()
