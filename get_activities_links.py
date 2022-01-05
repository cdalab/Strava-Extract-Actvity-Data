import json
import os
import time as t
import re
import random

import pandas as pd

from consts import *
from bs4 import BeautifulSoup
from utils import append_row_to_csv, log, timeout_wrapper
import threading
from browser import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Get_Activities_Links(Browser):

    def __init__(self, riders, id, csv_file_path):
        '''
        Params:
        -------
        riders - dataframe of riders STRAVA URLs
        id - some id to write in the log file (usually it is the ip address)
        csv_file_path - where to save all the riders_pages
        
        
        
        Extracts riders_pages from riders and saves it in the "csv_file_path" file
        Flow of action:
        1. run the "_create_links_for_extractions" to fetch all the dates where there are riders_pages
        2. run the "_fetch_links" to fetch all activity riders_pages for the riders_pages created in the "_create_links_for_extractions"
        
        To start the flow of action start the run() method.
        
        '''

        Browser.__init__(self, id)
        self.riders = riders
        self.csv_file_path = csv_file_path

    @timeout_wrapper
    def _get_rider_page(self, rider):
        self.browser.get(rider['strava_link'])
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        options_soup = soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
        first_link = soup.find(lambda tag: tag.name == "a" and "Monthly" in tag.text)
        t.sleep(random.random() + random.randint(0, 1))
        if options_soup and first_link:
            if (not os.path.exists(f"link/riders_pages/{rider['strava_id']}.html")):
                with open(f"link/riders_pages/{rider['strava_id']}.html", "a+") as f:
                    f.write(self.browser.page_source)
            extract_rider_perd = (not os.path.exists(self.csv_file_path))
            rider_in_csv_pred = (os.path.exists(self.csv_file_path) and (
                    rider['strava_id'] not in pd.read_csv(self.csv_file_path)['strava_id'].values))
            extract_rider_perd = extract_rider_perd or rider_in_csv_pred
            if extract_rider_perd:
                row = {'strava_id': rider['strava_id'],
                       'strava_link': rider['strava_link'],
                       'first_link': f"{BASE_STRAVA_URL}{first_link.attrs['href']}",
                       'options': str(options_soup).replace('\n', '')}
                append_row_to_csv(self.csv_file_path, row)
        else:
            raise TimeoutError(
                f'Elements have not located in page: options = {options_soup}, first link = {first_link}')

    def _get_rider_links(self):
        '''
        Fetch links of time intervals - for each time interval there is page full of activities. This method fetch those
        links and download the main html page of the riders.
        '''
        try:
            rider = None
            for i, rider in self.riders.iterrows():  # Fetch links for each rider
                extract_rider_perd = os.path.exists(self.csv_file_path) and (
                        rider['strava_id'] not in pd.read_csv(self.csv_file_path)['strava_id'].values)
                extract_rider_perd = extract_rider_perd or (not os.path.exists(
                    f"link/riders_pages/{rider['strava_id']}.html"))
                if extract_rider_perd:
                    log(f'Fetching page for cyclist {rider["full_name"]}, {i} / {len(self.riders)}', id=self.id)
                    t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch rider {rider["full_name"]}, id {rider["strava_id"]}.'
                    self._get_rider_page(link_fetch_error_msg, **dict(rider=rider))
        except:
            log(f'Failed fetching riders pages, current rider fetched {rider}', 'ERROR', id=self.id)



    def _get_rider_links(self,rider):
        try:
            row = {'strava_id': rider['strava_id'],
                   'time_interval_link': rider['first_link']}
            append_row_to_csv(self.csv_file_path, row)
            soup = BeautifulSoup(rider['options'], 'html.parser')
            options_soup = soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
            option_list = options_soup.find('ul','options').find_all('a')
            for time_interval in option_list:
                row = {'strava_id': rider['strava_id'],
                       'time_interval_link': f"{BASE_STRAVA_URL}{time_interval.attrs['href']}"}
                append_row_to_csv(self.csv_file_path, row)
        except:
            log(f'Could not fetch time interval links for rider {rider["strava_id"]}.','ERROR', id=self.id)



    def _extract_time_interval_links(self):

            try:
                rider_page = None
                for i, rider_page in self.riders.iterrows():  # Fetch links for each rider
                    csv_file_exist = os.path.exists(self.csv_file_path)
                    extract_rider_links_perd = (csv_file_exist and (rider_page['strava_id'] not in pd.read_csv(self.csv_file_path)['strava_id'].values))
                    if (not csv_file_exist) or extract_rider_links_perd:
                        log(f'Fetching time interval links for cyclist {rider_page["strava_id"]}, {i} / {len(self.riders)}', id=self.id)
                        self._get_rider_links(rider_page)
            except:
                log(f'Failed fetching riders time interval links, current rider fetched {rider_page}', 'ERROR', id=self.id)

    # soup = BeautifulSoup(self.browser.page_source, 'html.parser')
    # date_intervals = soup.find('div', {'class': 'drop-down-menu drop-down-sm enabled'})
    # temp_links = date_intervals.find_all('a')
    #
    # date_links = []
    # for temp_link in temp_links:
    #     link = self.STRAVA_URL + temp_link['href']
    #     link = link.replace('week', 'month')
    #     date_links.append(link)
    #
    # current_link_year = soup.find('h2', {'class': 'text-callout left'}).text[-5:-1]
    # current_link = date_links[0]
    # interval_exmaple = re.search("interval=.*&", current_link).group(0)
    # current_link = current_link.replace(interval_exmaple[-7:-3], current_link_year)
    # current_link = current_link[:-1] + '0'
    # date_links.insert(0, current_link)
    #
    # for link in date_links:
    #
    #     interval1 = re.search("interval=.*&", link).group(0)
    #     year = int(interval1[-7:-3])
    #
    #     if year-1 in rider.years:
    #
    #         for month in range(7,13):
    #             if month not in rider.months:
    #                 continue
    #
    #             month_string = str(month) if month >= 10 else f'0{month}'
    #             interval2 = interval1.replace(str(year)+interval1[-3:-1], str(year-1)+month_string)
    #             rider.links.append(link.replace(interval1, interval2))
    #
    #     if year in rider.years:
    #
    #         for month in range(1,8):
    #             if month not in rider.months:
    #                 continue
    #
    #             interval2 = interval1.replace(str(year)+interval1[-3:-1], str(year)+f'0{month}')
    #             rider.links.append(link.replace(interval1, interval2))

    def _fetch_links(self):

        '''
        Fetches links from each rider.links fetched from the previous method
        
        '''

        log(f'Total number of riders: {len(self.riders)}', 'info', id=self.id)
        for rider in self.riders:
            log(f'Fetching activity riders_pages for: {rider}', id=self.id)
            prev = set()
            curr = set()
            for link in rider.links:

                try:
                    year_link = int(re.search('interval=.*&', link).group(0)[9:-3])
                    if year_link not in rider.years:
                        continue

                    self.browser.get(link)
                    while self._is_logged_out():
                        self._switchAccount(link)
                        seconds_to_wait = 1800
                        log(f"IP BLOCKED - waiting for {seconds_to_wait} seconds...", id=self.id)
                        t.sleep(seconds_to_wait)

                    t.sleep(1)

                    timeout = t.time() + 10
                    new_curr = set()

                    while curr == prev:
                        t.sleep(1)
                        graph_soup = BeautifulSoup(self.browser.page_source, 'html.parser')

                        feed_activities = graph_soup.find_all('div', class_='react-card-container')
                        for activity in feed_activities:
                            links_a = activity.find_all('a')
                            for link_a in links_a:
                                if 'activities' in link_a['href']:
                                    new_curr.add(link_a['href'])
                                    break

                        curr = new_curr

                        if t.time() > timeout:
                            raise TimeoutError()

                    prev = curr
                    rider.activity_links = rider.activity_links.union(curr)

                    for l in curr:
                        row = {
                            'strava_id': rider.rider_id,
                            'workout_strava_id': l,
                        }
                        append_row_to_csv(self.csv_file_path, row, columns=['cyclist_id', 'workout_strava_id'])

                    if len(prev) > 0:
                        log(f'Found activities: {len(prev)}, year: {link[-20:-16]} month: {link[-16:-14]}', id=self.id)
                    else:
                        log(f'No activities, year: {link[-20:-16]} month: {link[-16:-14]}', 'INFO', id=self.id)


                except Exception as e:
                    log(f'Problem fetching activities from: {link}, {e}', 'ERROR', id=self.id)
                    continue
            log(f'finished rider: {rider.rider_id}, number of activities: {len(rider.activity_links)}', id=self.id)

        self._close_driver()

    def fetch_rider_links(self):
        '''
        Starts extract riders pages
        '''
        self._open_driver()
        self._get_rider_links()

    def fetch_rider_time_interval_links(self):
        '''
        Starts extract riders time interval links
        '''
        self._extract_time_interval_links()

# rider = Rider()
# lin = Get_Activities_Links()
