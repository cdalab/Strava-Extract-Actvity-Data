import time as t
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Get_Activities_Links():

    def __init__(self, username, riders, years = list(range(2015,2022)), months = list(range(1,13))):
        self.activity_links = set()
        self.riders = riders
        self.years = years
        self.months = months
        self.username = username
        self.STRAVA_URL = 'https://www.strava.com'

    def _open_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        URL = self.STRAVA_URL + '/login'

        self.browser.get(URL)
        email = self.browser.find_element_by_id("email")
        password = self.browser.find_element_by_id("password")

        email.send_keys(self.username)
        password.send_keys('12345678')

        self.browser.find_element_by_id("login-button").click()
        t.sleep(1)
        print(self.browser.current_url)

    def _close_driver(self):
        self.browser.close()

    def create_links_for_extractions(self):

        self._open_driver()
        problematic_riders = []
        for rider in self.riders:
            self.browser.get(rider.rider_url)
            t.sleep(1)
            print(rider)
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

        self.riders = [rider for rider in self.riders if rider not in problematic_riders]
        self._close_driver()

    def run(self):

        self._open_driver()


        for rider in self.riders:
            prev = set()
            curr = set()
            for link in rider.links:


                year_link = int(re.search('interval=.*&', link).group(0)[9:-3])
                if year_link not in self.years:
                    continue


                self.browser.get(link)
                site_soup = BeautifulSoup(self.browser.page_source, 'html.parser')

                if site_soup.find('html')['class'][0] == 'logged-out': # logged out ...
                    print(f'logged out...')
                    self._close_driver()
                    return

                #print(f'{self.browser.current_url}')
                t.sleep(2)
                timeout = t.time() + 10
                new_curr = set()

                while curr == prev:
                    t.sleep(1)
                    graph_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    group_feed_activities = graph_soup.find_all('div', {'class': 'feed-entry group-activity'})
                    normal_activities = graph_soup.find_all('div', {'class': 'activity feed-entry entity-details'})

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
                    curr = new_curr

                    if t.time() > timeout:
                        break

                prev = curr

                rider.activity_links = rider.activity_links.union(curr)
            print(f'finished rider: {rider.rider_id}, number of activities: {len(rider.activity_links)}')

        self._close_driver()