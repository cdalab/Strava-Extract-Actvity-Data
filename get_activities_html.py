
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

ACTIVITY_URL = 'https://www.strava.com/activities/'

class Get_Activities_HTML(Browser):
    
    
    def __init__(self, id, data=[]):
        '''
        data : Dictionary<RIDER_ID, Activity_ID>
        Example: {1: 6418596161}
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
        
        try:
            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            chart = analysis_soup.find_all('g', {'class': "label-box"})
            svg = analysis_soup.find_all('defs')
            before = t.time()
            dead_line = 6
            timeout = t.time() + dead_line
            too_much = t.time() + 60
            while len(chart) == 0 or len(svg) == 0: # Wait for load
                analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                chart = analysis_soup.find_all('g', {'class': "label-box"})
                svg = analysis_soup.find_all('defs')
                if t.time() > too_much:
                    return {}
                elif t.time() > timeout:
                    log(f'Cant Load Analysis Graphs: {self.curr_user} SWITCHING ACCOUNT', 'WARNING', id=self.id)
                    t.sleep(1)
                    self._switchAccount(analysis_url)
                    timeout = t.time() + dead_line

                t.sleep(0.1)
            after = t.time() - before
            print(f'loaded: {after}')
            analysis_distance_soup = analysis_soup
        
            try:
                time_button = self.browser.find_elements_by_tag_name('svg')[3].find_elements_by_tag_name('g')[25].find_elements_by_tag_name('image')[1]
                time_button.click()
                # print(time_button)
            #     # attrs=[]
            #     # for attr in time_button.get_property('attributes'):
            #     #     attrs.append([attr['name'], attr['value']])
            #     # print(attrs)
            #     webdriver.ActionChains(self.browser).move_to_element(time_button).send_keys(Keys.RETURN)
            #     t.sleep(1)
            #     # WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'g[data-type="time"]'))).send_keys(Keys.RETURN)

            #     # self.browser.execute_script("arguments[4].click();", time_button)
               
                # analysis_time_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            except Exception as e:
                print(e)
                analysis_time_soup = None
                
            
            analysis_time_soup = None
            
            return analysis_distance_soup, analysis_time_soup
            
        except Exception as e:
            log(f'BAD LINK: | {analysis_url} | {e}', 'WARNING', id=self.id)
        return None, None
            
    def get_generic_soup(self, home_url, extension):
            curr_url = home_url + extension
            
            self.browser.get(curr_url)
            t.sleep(0.5)
            self._check_if_too_many_requests(curr_url)

            
            try:
                gen_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                gen = gen_soup.find_all('tr')
                while len(gen) is None:
                    gen_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    gen = gen_soup.find_all('tr')
                    t.sleep(0.1)
                return gen_soup
            except Exception as e:
                log(f'BAD LINK: | {curr_url} | {e}', 'WARNING', id=self.id)
        
        
    def fetch_activity(self, activity_id, rider_id):
        
        home_url = ACTIVITY_URL + str(activity_id)
        
        
        t.sleep(0.5)
        self.browser.get(home_url)
        t.sleep(0.5)
        self._check_if_too_many_requests(home_url)
        home_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        
        
        # ==== CHECK IS MENU ITEMS EXIST ====
        analysis_exists = False
        zone_distribution_exists = False
        heart_rate_exists = False
        power_curve_exists = False
        
        try:
            site_menu = home_soup.find('ul', {'class': 'pagenav'}).find_all('a')
            for a in site_menu:
                if a['data-menu'] == 'analysis':
                    analysis_exists = True
                    break
        except:
            pass

        try:
            premium_views = home_soup.find('li', {'id': 'premium-views'}).find_all('a')
            for a in premium_views:
                if a['data-menu'] == 'heartrate':
                    heart_rate_exists = True
                if a['data-menu'] == 'zone-distribution':
                    zone_distribution_exists = True
                
                if a['data-menu'] == 'Power Curve':
                    power_curve_exists = True
        except:
            pass
        # ==================================

        
        
        analysis_distance_soup = None
        analysis_time_soup = None
        zone_distribution_soup = None
        heart_rate_soup = None
        power_curve_soup = None
        
        
        # Analysis soup
        if analysis_exists:
            analysis_distance_soup, analysis_time_soup = self.get_analysis_soup(home_url=home_url)
        
        if zone_distribution_exists:
            zone_distribution_soup = self.get_generic_soup(home_url=home_url, extension='/zone-distribution')
            
        if heart_rate_exists:
            heart_rate_soup = self.get_generic_soup(home_url=home_url, extension='/heartrate')
            
        if power_curve_exists:
            power_curve_soup = self.get_analysis_soup(home_url=home_url, extension='/power-curve')
            
            
     

        self.save_html(file_name="home", activity_id=activity_id, soup=home_soup)
        self.save_html(file_name="analysis_distance", activity_id=activity_id, soup=analysis_distance_soup)
        self.save_html(file_name="analysis_time", activity_id=activity_id, soup=analysis_time_soup)
        self.save_html(file_name="zone_distribution", activity_id=activity_id, soup=zone_distribution_soup)
        self.save_html(file_name="heart_rate", activity_id=activity_id, soup=heart_rate_soup)
        self.save_html(file_name="power_curve", activity_id=activity_id, soup=power_curve_soup)
        self.save_rider_id(activity_id=activity_id, rider_id=rider_id)
        
        
    def start(self):
        self._open_driver()
        total = len(self.data)
        i = 1
        for rider_id, activity_id in self.data:
            self.fetch_activity(activity_id, rider_id)
            msg = f'{i} / {total}'
            log(msg, id=self.id)
            i += 1
            
        
fetch = Get_Activities_HTML("test", [(1,6418596161)])
fetch.start()