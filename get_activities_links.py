import time as t
import re
from usernames import *
from bs4 import BeautifulSoup
from utils import append_row_to_csv, log
import threading
from browser import Browser

class Get_Activities_Links(threading.Thread, Browser):
    


    def __init__(self, riders, id, saving_file_name):
        '''
        Params:
        -------
        riders - list of Rider objects
        id - some id to write in the log file (usually it is the ip address)
        saving_file_name - where to save all the links
        
        
        
        Extracts links from riders and saves it in the "saving_file_name" file
        Flow of action:
        1. run the "_create_links_for_extractions" to fetch all the dates where there are links
        2. run the "_fetch_links" to fetch all activity links for the links created in the "_create_links_for_extractions"
        
        To start the flow of action start the run() method.
        
        '''
        
        
        
        Browser.__init__(self, id)
        self.activity_links = set()
        self.riders = riders
        self.saving_file_name = saving_file_name
        threading.Thread.__init__(self)


    def _create_links_for_extractions(self):
        
        '''
        In each rider there are time gaps in where links of activities are stored.
        This method fetches all the links where activity links are stored.
        
        '''

        problematic_riders = [] # save all riders whom cannot process links
        i = 1
        try:
            for rider in self.riders: # Fetch links for each rider
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

                        if year-1 in rider.years:

                            for month in range(7,13):
                                if month not in rider.months:
                                    continue

                                month_string = str(month) if month >= 10 else f'0{month}'
                                interval2 = interval1.replace(str(year)+interval1[-3:-1], str(year-1)+month_string)
                                rider.links.append(link.replace(interval1, interval2))

                        if year in rider.years:

                            for month in range(1,8):
                                if month not in rider.months:
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
                
                log(f'Problematic rider: {rider}', 'ERROR', id=self.id, dire='problematic_riders')
        self.riders = [rider for rider in self.riders if rider not in problematic_riders]
        

    def _fetch_links(self):
        
        '''
        Fetches links from each rider.links fetched from the previous method
        
        '''

        log(f'Total number of riders: {len(self.riders)}', 'info', id=self.id)
        for rider in self.riders:
            log(f'Fetching activity links for: {rider}', id=self.id)
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
                            'cyclist_id': rider.rider_id,
                            'workout_strava_id': l,
                        }
                        append_row_to_csv(self.saving_file_name, row, columns=['cyclist_id', 'workout_strava_id'])

                    if len(prev) > 0:
                        log(f'Found activities: {len(prev)}, year: {link[-20:-16]} month: {link[-16:-14]}', id=self.id)
                    else:
                        log(f'No activities, year: {link[-20:-16]} month: {link[-16:-14]}', 'INFO', id=self.id)
                        
                    
                except Exception as e:
                    log(f'Problem fetching activities from: {link}, {e}', 'ERROR', id=self.id)
                    continue
            log(f'finished rider: {rider.rider_id}, number of activities: {len(rider.activity_links)}', id=self.id)

        self._close_driver()

    def run(self):
        '''
        Starts the flow of actions
        '''
        self._open_driver()
        self._create_links_for_extractions()
        self._fetch_links()
        
 
# rider = Rider()
# lin = Get_Activities_Links()