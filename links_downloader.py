from bs4 import BeautifulSoup
from utils import *
from browser import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import parse_qsl
import time as t
import random


class LinksDownloader(Browser):

    def __init__(self, id, riders, html_files_path):
        Browser.__init__(self, id)
        self.riders = riders
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        year_offset = url_param_dict['year_offset']
        interval = url_param_dict['interval']
        interval_type = url_param_dict['interval_type']
        chart_type = url_param_dict['chart_type']
        html_file_name = f"{interval}_{interval_type}_{chart_type}_{year_offset}"
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    @timeout_wrapper
    def _download_rider_page(self, rider):
        self.browser.get(rider['strava_link'])
        t.sleep(random.random() + random.randint(0, 1))
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        options_soup = soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
        first_link = soup.find(lambda tag: tag.name == "a" and "Weekly" in tag.text)
        url_param_dict = dict(parse_qsl(first_link.attrs['href'].split('?')[1]))
        if options_soup and first_link:
            html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider['strava_id'],
                                                                                 url_param_dict)
            write_to_html(html_file_dir, html_file_name, self.browser.page_source)
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
                    log(f'Fetching page for cyclist {rider["full_name"]}, {i} / {len(self.riders) - 1}', id=self.id)
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
        current_interval_range_element = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, "interval-value")))
        current_interval_range = current_interval_range_element.text
        if prev_interval_range == current_interval_range:
            raise ValueError(f'The relevant interval page has not loaded yet')
        self.browser.switch_to.parent_frame()
        feed = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "feed")))
        num_of_activities = len(feed.find_elements(By.XPATH, "./*"))
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
                write_to_html(html_file_dir, html_file_name, self.browser.page_source)
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
                url_param_dict = dict(parse_qsl(r_year_interval['time_interval_link'].split('?')[1]))
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(r_year_interval['strava_id'],
                                                                                     url_param_dict)
                if not os.path.exists(f"{html_file_dir}/{html_file_name}.html"):
                    log(f'Fetching page for cyclist {r_year_interval["strava_id"]}, file {html_file_name}, {i} / {len(self.riders) - 1}',
                        id=self.id)
                    # t.sleep(random.random())
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
                url_param_dict = dict(parse_qsl(r_week_interval['time_interval_link'].split('?')[1]))
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(r_week_interval['strava_id'],
                                                                                     url_param_dict)
                if not os.path.exists(f"{html_file_dir}/{html_file_name}.html"):
                    log(f'Fetching page for cyclist {r_week_interval["strava_id"]}, file {html_file_name}, {i} / {len(self.riders) - 1}',
                        id=self.id)
                    # t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch week interval {r_week_interval["time_interval_link"]}, for rider {r_week_interval["strava_id"]}.'
                    prev_week_interval_range = self._download_rider_time_interval_page(link_fetch_error_msg,
                                                                                       url_param_dict,
                                                                                       prev_week_interval_range,
                                                                                       **dict(
                                                                                           rider_time_interval=r_week_interval))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {r_week_interval}', 'ERROR', id=self.id)

    # TODO : handle 'indoor cycling' when extract activity data
    @timeout_wrapper
    def _download_rider_activity_pages(self, prev_activity, i, rider_activity):
        self.browser.get(rider_activity['activity_link'])
        t.sleep(random.random() + 0.5 + random.randint(1, 3))
        heading = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "heading")))
        details = WebDriverWait(heading, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "details")))
        current_activity_title = details.text
        activity_details = WebDriverWait(heading, 2).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "ul")))
        current_activity = ''.join([ad.text for ad in activity_details]) + current_activity_title
        if prev_activity == current_activity:
            raise ValueError(f'The relevant activity page has not loaded yet')
        activity_type = WebDriverWait(heading, 7).until(EC.visibility_of_element_located((By.TAG_NAME, "h2")))
        if ("Ride" not in activity_type.text) and ("Cycling" not in activity_type.text):
            return current_activity
        log(f'Fetching activity page for cyclist {rider_activity["strava_id"]}, activity {rider_activity["activity_id"]}, {i} / {len(self.riders) - 1}',
            id=self.id)
        WebDriverWait(heading, 7).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
        html_file_dir = f"{self.html_files_path}/{rider_activity['strava_id']}/{rider_activity['activity_id']}"
        write_to_html(html_file_dir, "overview", self.browser.page_source)
        return current_activity

    @driver_wrapper
    def download_activity_pages(self):
        try:
            activity = None
            prev_activity = None
            i = 0
            for idx, activity in self.riders.iterrows():
                html_file_dir = f"{self.html_files_path}/{activity['strava_id']}/{activity['activity_id']}"
                if not os.path.exists(f"{html_file_dir}/overview.html"):
                    # t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch activity {activity["activity_id"]}, for rider {activity["strava_id"]}.'
                    prev_activity = self._download_rider_activity_pages(link_fetch_error_msg,
                                                                        prev_activity, i,
                                                                        **dict(
                                                                            rider_activity=activity))
                i += 1
        except:
            log(f'Failed fetching riders activity pages, current activity fetched {activity}.', 'ERROR', id=self.id)
