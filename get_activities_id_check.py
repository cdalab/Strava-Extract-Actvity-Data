from pathlib import Path
import time as t
from browser import Browser
from bs4 import BeautifulSoup
from utils import log
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd

BASE_URL = 'https://www.strava.com/'


class Get_Activities_id_check(Browser):

    def __init__(self, id, data=[]):
        '''
        data : Dictionary<RIDER_ID, Activity_ID>
        Example: {1: 6418596161}
        '''

        super().__init__(id)
        self.data = data

    def start(self):
        self._open_driver()
        total = len(self.data)
        i = 1
        # result_df = pd.DataFrame(columns=['cyclist_id', 'cyclist_name', 'cyclist_url', 'strava_name'])
        # result_df.to_csv('result_df.csv', index=False, header=True)
        for cyclist_id, cyclist_name, cyclist_url in self.data:
            if str(cyclist_url) == 'nan':
                msg = f'{i} / {total}'
                log(msg, id=self.id)
                i += 1
                continue
            t.sleep(0.5)
            if ('https://' not in cyclist_url) and ('http://' not in cyclist_url):
                cyclist_url='https://'+cyclist_url
            self.browser.get(cyclist_url)
            t.sleep(0.5)
            self._check_if_too_many_requests(cyclist_url)
            home_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            try:
                strava_name = home_soup.find('h1').text
            except:
                strava_name = None
            df = pd.DataFrame([dict(cyclist_id=cyclist_id, cyclist_name=cyclist_name, cyclist_url=cyclist_url,
                                   strava_name=strava_name)])
            df.to_csv('result_df.csv', mode='a', index=False, header=False)
            msg = f'{i} / {total}'
            log(msg, id=self.id)
            i += 1
