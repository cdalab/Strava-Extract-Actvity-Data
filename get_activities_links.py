import json
import os
import time as t
import re
import random
from pathlib import Path

import pandas as pd

from consts import *
from bs4 import BeautifulSoup
from utils import *
import threading
from browser import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import parse_qsl


class Links_Extractor(Browser):

    def __init__(self, id, riders, html_files_path):
        Browser.__init__(self, id)
        self.riders = riders
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        html_file_name = "_".join(url_param_dict.values())
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    def _fetch_rider_year_interval_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_html_file = os.listdir(rider_dir_path)[0]
            with open(f"{rider_dir_path}/{rider_html_file}") as f:
                rider_soup = BeautifulSoup(f.read(), 'html.parser')
                options_soup = rider_soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
                option_list = options_soup.find('ul', 'options').find_all('a')
                for time_interval in option_list:
                    row = {'strava_id': rider_id,
                           'time_interval_link': f"{BASE_STRAVA_URL}{time_interval.attrs['href']}"}
                    append_row_to_csv(csv_file_path, row)
        except:
            log(f'Could not fetch year interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_year_interval_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.riders:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values):
                    log(f'Fetching year interval links for cyclist {rider_id}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    self._fetch_rider_year_interval_links(rider_id, csv_file_path)
                i += 1
        except:
            log(f'Failed fetching riders year interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_week_interval_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_year_interval_files = os.listdir(rider_dir_path)
            i = 0
            for year_interval_link in rider_year_interval_files:
                log(f'Fetching week interval links from file {year_interval_link}, {i} / {len(rider_year_interval_files)-1}',
                    id=self.id, debug=False)
                with open(f"{rider_dir_path}/{year_interval_link}") as f:
                    rider_soup = BeautifulSoup(f.read(), 'html.parser')
                    rider_intervals = rider_soup.find('ul', attrs={'class': 'intervals'}).find_all('a')
                    for week_interval in rider_intervals:
                        row = {'strava_id': rider_id,
                               'time_interval_link': f"{BASE_STRAVA_URL}{week_interval.attrs['href']}"}
                        append_row_to_csv(csv_file_path, row)
                i = +1
        except:
            log(f'Could not fetch week interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_week_interval_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.riders:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values):
                    log(f'Fetching week interval links for cyclist {rider_id}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    self._fetch_rider_week_interval_links(rider_id, csv_file_path)
                i += 1
        except:
            log(f'Failed fetching riders week interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_activity_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_html_file = os.listdir(rider_dir_path)[0]
            with open(f"{rider_dir_path}/{rider_html_file}") as f:
                rider_soup = BeautifulSoup(f.read(), 'html.parser')
                activities_soup = rider_soup.find('div', attrs={'class': 'feed'})
                activities_list = activities_soup.find_all('div', attrs={
                    'class': 'react-card-container'})
                for activity_card in activities_list:
                    activity_a = activity_card.find(lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
                    if activity_a is not None:
                        activity_link = f"{BASE_STRAVA_URL}{activity_a.attrs['href']}"
                        activity_id = activity_link.split('/activities/')[1]
                        row = {'strava_id': rider_id,
                               'activity_link': activity_link,
                               'activity_id': activity_id}
                        append_row_to_csv(csv_file_path, row)
                    else:
                        challenge = activity_card.find(
                            lambda tag: tag.name == "a" and "/challenges/" in tag.attrs['href'])
                        if challenge is None:
                            raise ValueError('Activity card type is not recognized')
        except:
            log(f'Could not fetch time interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_activity_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.riders:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values):
                    log(f'Fetching time interval links for cyclist {rider_id}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    self._fetch_rider_activity_links(rider_id, csv_file_path)
                i += 1

        except:
            log(f'Failed fetching rider activity links, current rider fetched {rider_id}', 'ERROR',
                id=self.id)


class Links_Downloader(Browser):

    def __init__(self, id, riders, html_files_path):
        Browser.__init__(self, id)
        self.riders = riders
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        html_file_name = "_".join(url_param_dict.values())
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    @timeout_wrapper
    def _download_rider_page(self, rider):
        self.browser.get(rider['strava_link'])
        t.sleep(random.random() + random.randint(0, 1))
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        options_soup = soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
        first_link = soup.find(lambda tag: tag.name == "a" and "Weekly" in tag.text)
        url_param_dict = dict(parse_qsl(first_link.attrs['href']))
        if options_soup and first_link:
            html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider['strava_id'],
                                                                                 url_param_dict)
            Path(html_file_dir).mkdir(parents=True, exist_ok=True)
            if (not os.path.exists(f"{html_file_dir}/{html_file_name}.html")):
                with open(f"{html_file_dir}/{html_file_name}.html", "w+") as f:
                    f.write(self.browser.page_source)
        else:
            raise TimeoutError(
                f'Elements have not located in page: options = {options_soup}, first link = {first_link}')

    @driver_wrapper
    def download_rider_pages(self):
        try:
            rider = None
            i = 0
            for idx, rider in self.riders.iterrows():  # Fetch links for each rider
                html_file_dir = f"{self.html_files_path}/{rider['strava_id']}"
                if not os.path.exists(html_file_dir):
                    log(f'Fetching page for cyclist {rider["full_name"]}, {i} / {len(self.riders)-1}', id=self.id)
                    t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch rider {rider["full_name"]}, id {rider["strava_id"]}.'
                    self._download_rider_page(link_fetch_error_msg,
                                              **dict(rider=rider))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {rider}', 'ERROR', id=self.id)

    @timeout_wrapper
    def _download_rider_time_interval_page(self, url_param_dict, prev_interval_range,
                                           rider_time_interval):
        self.browser.get(rider_time_interval['time_interval_link'])
        t.sleep(random.random() + 0.5 + random.randint(2, 4))
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, "interval-value")))
        current_interval_range = self.browser.find_element_by_id("interval-value").text
        if prev_interval_range == current_interval_range:
            raise ValueError(f'The relevant interval page has not loaded yet')
        self.browser.switch_to.parent_frame()
        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "feed")))
        num_of_activities = len(self.browser.find_element_by_class_name("feed").find_elements_by_xpath("./*"))
        if num_of_activities > 0:
            WebDriverWait(self.browser, 5).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "react-card-container")))
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        activities_soup = soup.find('div', attrs={'class': 'feed'})
        activities_soup_list = activities_soup.find_all('div', attrs={
            'class': 'react-card-container'}) if activities_soup else None
        if activities_soup_list is not None:
            html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider_time_interval['strava_id'],
                                                                                 url_param_dict)
            Path(html_file_dir).mkdir(parents=True, exist_ok=True)
            # TODO: remove true or
            if True or (not os.path.exists(f"{html_file_dir}/{html_file_name}.html")):
                with open(f"{html_file_dir}/{html_file_name}.html", "w+") as f:
                    f.write(self.browser.page_source)
            # TODO: to remove, it is a test to see if the first page (year) identical to week interval calc later
            else:
                print('')
            return current_interval_range
        else:
            raise TimeoutError(
                f'Element have not located in page: activities = {activities_soup}')

    @driver_wrapper
    def download_year_interval_pages(self):
        try:
            r_year_interval = None
            prev_year_interval_range = None
            i = 0
            for idx, r_year_interval in self.riders.iterrows():
                url_param_dict = dict(parse_qsl(r_year_interval['time_interval_link']))
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(r_year_interval['strava_id'],
                                                                                     url_param_dict)
                if not os.path.exists(f"{html_file_dir}/{html_file_name}.html"):
                    log(f'Fetching page for cyclist {r_year_interval["strava_id"]}, file {html_file_name}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch year interval {r_year_interval["time_interval_link"]}, for rider {r_year_interval["strava_id"]}.'
                    prev_year_interval_range = self._download_rider_time_interval_page(link_fetch_error_msg,
                                                                                       url_param_dict,
                                                                                       prev_year_interval_range,
                                                                                       **dict(
                                                                                           rider_time_interval=r_year_interval))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {r_year_interval}', 'ERROR', id=self.id)

    @driver_wrapper
    def download_week_interval_pages(self):
        try:
            r_week_interval = None
            prev_week_interval_range = None
            i = 0
            for idx, r_week_interval in self.riders.iterrows():
                url_param_dict = dict(parse_qsl(r_week_interval['time_interval_link']))
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(r_week_interval['strava_id'],
                                                                                     url_param_dict)
                #TODO: remove true or
                if True or (not os.path.exists(f"{html_file_dir}/{html_file_name}.html")):
                    log(f'Fetching page for cyclist {r_week_interval["strava_id"]}, file {html_file_name}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch week interval {r_week_interval["time_interval_link"]}, for rider {r_week_interval["strava_id"]}.'
                    prev_week_interval_range = self._download_rider_time_interval_page(link_fetch_error_msg,
                                                                                          url_param_dict,
                                                                                          prev_week_interval_range,
                                                                                          **dict(
                                                                                              rider_time_interval=r_week_interval))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {r_week_interval}', 'ERROR', id=self.id)

    @timeout_wrapper
    def _download_rider_activity_pages(self, prev_activity_title, rider_activity):
        self.browser.get(rider_activity['activity_link'])
        t.sleep(random.random() + 0.5 + random.randint(2, 4))
        WebDriverWait(self.browser, 7).until(EC.presence_of_element_located((By.CLASS_NAME, "details")))
        # TODO : check if it is contains the title + date
        current_activity_title = self.browser.find_element_by_class_name("details").text
        if prev_activity_title == current_activity_title:
            raise ValueError(f'The relevant activity page has not loaded yet')
        self.browser.switch_to.parent_frame()
        WebDriverWait(self.browser, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, "spans8 activity-stats mt-md mb-md")))
        WebDriverWait(self.browser, 7).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "ul")))
        WebDriverWait(self.browser, 7).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
        html_file_dir = f"{self.html_files_path}/{rider_activity['strava_id']}"
        Path(html_file_dir).mkdir(parents=True, exist_ok=True)
        activity_file_path = f"{html_file_dir}/{rider_activity['activity_id']}.html"
        if (not os.path.exists(activity_file_path)):
            with open(activity_file_path, "w+") as f:
                f.write(self.browser.page_source)
        return current_activity_title

    @driver_wrapper
    def download_activity_pages(self):
        try:
            activity = None
            prev_activity_title = None
            i = 0
            for idx, activity in self.riders.iterrows():

                if not os.path.exists(f"{activity['activity_id']}.html"):
                    log(f'Fetching activity page for cyclist {activity["strava_id"]}, activity {activity["activity_id"]}, {i} / {len(self.riders)-1}',
                        id=self.id)
                    t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch activity {activity["activity_id"]}, for rider {activity["strava_id"]}.'
                    prev_activity_title = self._download_rider_activity_pages(link_fetch_error_msg,
                                                                                 prev_activity_title,
                                                                                 **dict(
                                                                                     rider_activity=activity))
                i += 1
        except:
            log(f'Failed fetching riders activity pages, current activity fetched {activity}.', 'ERROR', id=self.id)
