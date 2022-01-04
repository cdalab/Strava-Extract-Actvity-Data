
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
import os
import glob


ACTIVITY_URL = 'https://www.strava.com/activities/'
STRAVA_URL = 'https://www.strava.com'

class Get_Activities_HTML(Browser):
    
    
    def __init__(self, id, data=[]):
        '''
        data : List<RIDER_ID, Activity_ID>
        Example: [(1,6418596161), (2,6432917402)]
        '''

        super().__init__(id)
        self.data = data
        
    def save_html(self, file_name, activity_id, soup):
        if soup is None:
            return
        directory = f"html/{activity_id}/"
        Path(f"{directory}").mkdir(parents=True, exist_ok=True)
        with open(f"{directory}/{file_name}.html", "w", encoding='utf-8') as file:
            file.write(str(soup))
    
    def save_rider_id(self, activity_id, rider_id):
        directory = f"html/{activity_id}/"
        Path(f"{directory}").mkdir(parents=True, exist_ok=True)
        with open(f"{directory}/data.txt", "w", encoding='utf-8') as file:
            file.write(f"cyclist_id:{rider_id}")
        
            
            
    def get_analysis_soup(self, home_url):
        analysis_url = home_url + '/analysis'
        t.sleep(0.5)
        self.browser.get(analysis_url)
        t.sleep(0.5)
        self._check_if_too_many_requests(analysis_url)
        analysis_distance_soup, analysis_time_soup = None, None 
        try:
            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            chart = analysis_soup.find_all('g', {'class': "label-box"})
            svg = analysis_soup.find_all('defs')
            dead_line = 6
            timeout = t.time() + dead_line
            too_much = t.time() + 60
            while len(chart) == 0 or len(svg) == 0: # Wait for load
                analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                chart = analysis_soup.find_all('g', {'class': "label-box"})
                svg = analysis_soup.find_all('defs')
                if t.time() > too_much:
                    raise TimeoutError()
                elif t.time() > timeout:
                    log(f'Cant Load Analysis Graphs: {self.curr_user} SWITCHING ACCOUNT', 'WARNING', id=self.id)
                    t.sleep(1)
                    self._switchAccount(analysis_url)
                    timeout = t.time() + dead_line

                t.sleep(0.1)
            
            
            analysis_distance_soup = analysis_soup
            try:
                time_button = self.browser.find_element_by_css_selector("#stacked-chart > div > svg > g.xaxis-container > g.chart-controls > g:nth-child(2) > image")
                time_button.click()
                t.sleep(0.5)
                analysis_time_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            except:
                log(f'BAD LINK: | {analysis_url} | Failed to click on time button', 'ERROR', id=self.id)
                
            
        except Exception as e:
            log(f'BAD LINK: | {analysis_url} | {e}', 'ERROR', id=self.id)
            
        return analysis_distance_soup, analysis_time_soup
            
    def get_generic_soup(self, home_url, extension, object_to_find, object_string, object_attributes={}, find_object=True):
            curr_url = home_url + extension
            
            t.sleep(0.5)
            self.browser.get(curr_url)
            t.sleep(0.5)
            self._check_if_too_many_requests(curr_url)
            
            
            if self.browser.current_url == home_url:
                # Page does not exists
                return None

            if not find_object:
                return BeautifulSoup(self.browser.page_source, 'html.parser')
            
            
            try:
                gen_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                gen = gen_soup.find_all(object_to_find, string=object_string, attrs=object_attributes)
                timeout = t.time() + 10
                while len(gen) is None and t.time() < timeout:
                    gen_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    gen = gen_soup.find_all(object_to_find, string=object_string, attrs=object_attributes)
                    t.sleep(0.1)
                    
                if t.time() > timeout:
                    raise TimeoutError()
                if len(gen) == 0:
                    return None
                else:
                    return gen_soup
            except Exception as e:
                log(f'BAD LINK: | {curr_url} | {e}', 'ERROR', id=self.id)
        
        
    def fetch_activity(self, activity_id, rider_id):
        
        home_url = ACTIVITY_URL + str(activity_id)
        
        
        t.sleep(0.5)
        self.browser.get(home_url)
        t.sleep(0.5)
        self._check_if_too_many_requests(home_url)
        
        home_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        analysis_distance_soup, analysis_time_soup = self.get_analysis_soup(home_url=home_url)
        zone_distribution_soup = self.get_generic_soup(home_url=home_url, extension='/zone-distribution', object_to_find='h2', object_string='Zone Distribution')
        heart_rate_soup = self.get_generic_soup(home_url=home_url, extension='/heartrate', object_to_find='h2', object_string='Heart Rate Analysis')
        power_curve_soup = self.get_generic_soup(home_url=home_url, extension='/power-curve', object_to_find='h2', object_string='Power Curve')
        est_power_curve_soup = self.get_generic_soup(home_url=home_url, extension='/est-power-curve', object_to_find='h2', object_string='Estimated Power Curve', object_attributes={'class':'float-left'})
        power_distribution_soup = self.get_generic_soup(home_url=home_url, extension='/power-distribution', object_to_find='div', object_string=None, object_attributes={'id':'power-dist-chart'})
        laps_soup = self.get_generic_soup(home_url=home_url, extension='/laps', object_to_find='section', object_string=None, object_attributes={'id':'efforts-table'})
    
        
        self.save_html(file_name="home", activity_id=activity_id, soup=home_soup)
        self.save_html(file_name="analysis_distance", activity_id=activity_id, soup=analysis_distance_soup)
        self.save_html(file_name="analysis_time", activity_id=activity_id, soup=analysis_time_soup)
        self.save_html(file_name="zone_distribution", activity_id=activity_id, soup=zone_distribution_soup)
        self.save_html(file_name="heart_rate", activity_id=activity_id, soup=heart_rate_soup)
        self.save_html(file_name="power_curve", activity_id=activity_id, soup=power_curve_soup)
        self.save_html(file_name="est_power_curve", activity_id=activity_id, soup=est_power_curve_soup)
        self.save_html(file_name="power_distribution", activity_id=activity_id, soup=power_distribution_soup)
        self.save_html(file_name="laps", activity_id=activity_id, soup=laps_soup)
        self.save_rider_id(activity_id=activity_id, rider_id=rider_id)
        
        
        # ===== links that we didn't think about ======
        
        premium_sections = home_soup.find("li", {"id": "premium-views"})
        if premium_sections is not None:
            premium_sections = premium_sections.find_all("li")
        
            not_to_download = ['zone-distribution', 'heartrate', 'power-curve', 'est-power-curve', 'power-distribution']
            for section in premium_sections:
                link_a = section.find("a")
                if link_a is None:
                    continue
                
                link_name = link_a["href"].split("/")[-1]
                if link_name in not_to_download:
                    continue
                
                unknown_soup = self.get_generic_soup(home_url=home_url, extension=f'/{link_name}', object_to_find=None, object_string=None, object_attributes=None, find_object=False)
                self.save_html(file_name=f"{link_name}", activity_id=activity_id, soup=unknown_soup)

        # ==============================================
        
        
        # ============= download GPX FILE =============
        GPX_link = ''
        open_menu_items = home_soup.find('div', class_=['slide-menu','drop-down-menu', 'enabled','align-bottom']).find_all('a')
        for menu in open_menu_items:
            if  menu.text == 'Export GPX':
                GPX_link = STRAVA_URL + menu['href']
                break
        
        def delete_gpx_files():
            gpx_files = glob.glob('downloads/*.gpx')
            for gpx_file in gpx_files:
                os.remove(gpx_file)
        
        try:
            if not GPX_link == '':
                delete_gpx_files() # Delete file to avoid issues with id belonging
                self.browser.get(GPX_link)
                timeout = t.time() + 10 # Wait 10 seconds to download file
                while len(glob.glob('downloads/*.gpx')) == 0 and t.time() < timeout:
                    t.sleep(1)
                
                if len(glob.glob('downloads/*.gpx')) == 1:
                    # downloaded file
                    # move to our folder
                    gpx_file = glob.glob('downloads/*.gpx')[0]
                    os.rename(gpx_file, f'html/{activity_id}/gpx_file.gpx')
                    delete_gpx_files()
        # =============================================
                
        except Exception as e:
            log(f'Problem downlading GPX file {home_url}, {e}', 'ERROR', id=self.id)
        
        
        
        
    def start(self):
        self._open_driver()
        total = len(self.data)
        i = 1
        for rider_id, activity_id in self.data:
            start = t.time()
            self.fetch_activity(activity_id, rider_id)
            end = t.time()
            
            msg = f'Progress: | {i} / {total} | Duration: | {round(end-start, 3)} |'
            log(msg, 'INFO',id=self.id)
            i += 1
            
        
        

fetch = Get_Activities_HTML("test", [(2,6432917402), (1,6418596161), (3, 6469654111)])
fetch.start()