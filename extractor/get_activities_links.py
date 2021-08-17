import time as t
import re
import random
from usernames import *
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils import log

class Get_Activities_Links():

    def __init__(self, riders, id, years = tuple(range(2015,2022)), months = tuple(range(1,13))):
        self.activity_links = set()
        self.id = id
        self.riders = riders
        self.years = years
        self.months = months
        self.STRAVA_URL = 'https://www.strava.com'
        self.curr_user = ''

    def _switchAccount(self, url_to_refresh):
        self._close_driver()
        self._open_driver()
        self.browser.get(url_to_refresh)
        t.sleep(0.5)

    def _is_logged_out(self):
        site_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        try:
            if site_soup.find('html')['class'][0] == 'logged-out': # logged out ...
                log(f'logged out. username: {self.curr_user}', 'ERROR', id=self.id)
                return True
            else:
                return False
        except:
            return False

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
        if not self.browser.current_url == 'https://www.strava.com/onboarding':
            # BAD ACCOUNT! need
            log(f"BAD ACCOUNT {user} - Switching to another", id=self.id)
            self._close_driver()
            self._open_driver()
        elif self.browser.current_url == 'https://www.strava.com/login':
            # ip blocked...
            seconds_to_wait = 300
            log(f"IP BLOCKED - waiting for {seconds_to_wait} seconds...", id=self.id)
            self._close_driver()
            t.sleep(seconds_to_wait)
            self._open_driver()
        else:
            log(self.browser.current_url, id=self.id)


    def _close_driver(self):
        self.browser.close()

    def create_links_for_extractions(self):

        self._open_driver()
        problematic_riders = []
        i = 1
        try:
            for rider in self.riders:
                self.browser.get(rider.rider_url)
                log(f'Fetching links for extractions {i} / {len(self.riders)}', id=self.id)
                t.sleep(1)

                try:

                    soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    date_intervals = soup.find('div', {'class': 'drop-down-menu drop-down-sm enabled'})
                    temp_links = date_intervals.find_all('a')

                    date_links = []
                    for temp_link in temp_links:
                        link = self.STRAVA_URL + temp_link['href']
                        link = link.replace('week', 'month')
                        date_links.append(link)

                    current_link_year = soup.find('h2', {'class': 'text-callout left'}).text[-5:-1]
                    current_link = date_links[0]
                    interval_exmaple = re.search("interval=.*&", current_link).group(0)
                    current_link = current_link.replace(interval_exmaple[-7:-3], current_link_year)
                    current_link = current_link[:-1] + '0'
                    date_links.insert(0, current_link)

                    for link in date_links:

                        interval1 = re.search("interval=.*&", link).group(0)
                        year = int(interval1[-7:-3])

                        if year-1 in self.years:

                            for month in range(7,13):
                                if month not in self.months:
                                    continue

                                month_string = str(month) if month >= 10 else f'0{month}'
                                interval2 = interval1.replace(str(year)+interval1[-3:-1], str(year-1)+month_string)
                                rider.links.append(link.replace(interval1, interval2))

                        if year in self.years:

                            for month in range(1,8):
                                if month not in self.months:
                                    continue

                                interval2 = interval1.replace(str(year)+interval1[-3:-1], str(year)+f'0{month}')
                                rider.links.append(link.replace(interval1, interval2))

                except:
                    problematic_riders.append(rider)
                finally:
                    i += 1
        except:
            log(f'Unexpected error...', 'ERROR', id=self.id)
        if len(problematic_riders) > 0:
            for rider in problematic_riders:
                log(f'Problematic rider: {rider}', 'ERROR', id=self.id)
        self.riders = [rider for rider in self.riders if rider not in problematic_riders]
        self._close_driver()

    def run(self):

        self._open_driver()
        for rider in self.riders:
            log(f'Fetching activity links for: {rider}', id=self.id)
            prev = set()
            curr = set()
            for link in rider.links:

                try:
                    year_link = int(re.search('interval=.*&', link).group(0)[9:-3])
                    if year_link not in self.years:
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
                        group_feed_activities = graph_soup.find_all('div', {'class': 'feed-entry group-activity'})
                        normal_activities = graph_soup.find_all('d-iv', {'class': 'activity feed-entry entity-details'})
                        group_photo_and_map_activities = graph_soup.find_all('div', {'class': 'PhotosAndMapImage--entry-image-wrapper--ZHw4O'})

                        for group_feed_activity in group_feed_activities:
                            # loop through all group activities
                            group_feed_entry_body = group_feed_activity.find('div', {'class': 'entry-body'})
                            group_feed_link = group_feed_entry_body.find('a')
                            try:
                                new_curr.add(self.STRAVA_URL + group_feed_link.get('href'))
                            except:

                                continue

                        for normal_activity in normal_activities:
                            # loop through all normal activities
                            normal_activity_entry_body = normal_activity.find('div', {'class': 'entry-body'})
                            normal_activity_link = normal_activity_entry_body.find('a')
                            try:
                                new_curr.add(self.STRAVA_URL + normal_activity_link.get('href'))
                            except:

                                continue

                        for photo_and_map in group_photo_and_map_activities:
                            photo_map_activity_link = photo_and_map.find('a')
                            try:
                                new_curr.add(self.STRAVA_URL + photo_map_activity_link.get('href'))
                            except:
                                continue
                        curr = new_curr

                        if t.time() > timeout:
                            break

                    prev = curr
                    rider.activity_links = rider.activity_links.union(curr)
                    if len(prev) > 0:
                        log(f'Found activities: {len(prev)}, year: {link[-20:-16]} month: {link[-16:-14]}', id=self.id)
                    else:
                        log(f'No activities, year: {link[-20:-16]} month: {link[-16:-14]}', 'ERROR', id=self.id)
                except Exception as e:
                    log(f'Problem fetching activities from: {link}, {e}', 'ERROR', id=self.id)
                    continue
            log(f'finished rider: {rider.rider_id}, number of activities: {len(rider.activity_links)}', id=self.id)

        self._close_driver()