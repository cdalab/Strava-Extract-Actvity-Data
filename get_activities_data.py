import time as t
import re
from datetime import datetime
from bs4 import BeautifulSoup
from browser import Browser
from utils import *
from usernames import *



LOGIN_URL = 'https://www.strava.com/login'



class Get_Activities_Data(Browser):

    def __init__(self, riders, id, saving_file_name, start_from_index = 0):
        super().__init__(id)
        
        self.riders = riders
        self.start_from_index = start_from_index
        self.saving_file_name = saving_file_name
        self.folder_name = 'info'
        

    def _extract_activity_home(self, url):
        data = {}
        t.sleep(0.5)
        self.browser.get(url)
        t.sleep(0.5)
        self._check_if_too_many_requests(url)
        # print(self.browser.current_url)

        activity_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        try:
            data['type'] = activity_soup.find('span', {'class': 'title'}).text.split('\n')[-2]
        except:
            pass
        data['workout_strava_id'] = re.findall('.*/([0-9]+)$',url)[0]

        strong_data = activity_soup.find_all("strong")
        strong_data = BeautifulSoup(str(strong_data), "html.parser").get_text()
        strong_data.split('\\n')
        strong_data = strong_data.strip('][').split(', ')
        strong_data = list(map(lambda x:x.strip("\n"), strong_data))

        strong_data_labels = activity_soup.find_all('div', {'class': 'label'})
        strong_data_labels = BeautifulSoup(str(strong_data_labels), "html.parser").get_text()
        strong_data_labels = strong_data_labels.split('\\n')
        strong_data_labels = strong_data_labels[0].strip('][').split(', ')
        strong_data_labels = list(map(lambda x:x.strip("\n").lower(), strong_data_labels))

        strong_dict = dict(zip(strong_data_labels, strong_data))

        if 'distance' in strong_dict.keys():
            try:
                data['distance'] = float(strong_dict['distance'][:-2])*1609.34
            except:
                pass


        if 'moving time' in strong_dict.keys():
            try:
                time = strong_dict['moving time'].split(':')
                total_time = 0
                for i in range(len(time)):
                    total_time += int(re.sub("[^0-9]", "", time[i]))/(60**i)
                data['total_time'] = total_time
            except:
                pass


        if 'relative effort' in strong_dict.keys():
            try:
                data['relative_effort'] = float(strong_dict['relative effort'])
            except:
                pass


        if 'total work' in strong_dict.keys():
            try:
                data['energy'] = float(strong_dict['total work'][:-2].replace(',', ''))
            except:
                pass

        if 'training load' in strong_dict.keys():
            try:
                data['training_load'] = float(strong_dict['training load'])
            except:
                pass


        if 'intensity' in strong_dict.keys():
            try:
                data['intensity'] = float(strong_dict['intensity'][:-1])/100
            except:
                pass


        if 'relative effort' in strong_dict.keys():
            try:
                data['relative_effort'] = float(strong_dict['relative effort'])
            except:
                pass


        date = activity_soup.find('time').text.replace('\n', '')
        date_formats = ['%A, %d %B %Y', '%A, %d %B, %Y', '%A, %B %d %Y', '%A, %B %d, %Y']
        for date_format in date_formats:
            try:
                date = datetime.strptime(date, date_format)
                data['workout_datetime'] = date
                data['workout_week'] = date.isocalendar()[1]
                data['workout_month'] = date.month
                break
            except Exception as e:
                continue
        #data['temp_avg'] = (float(re.sub('\D', '', activity_soup.find('div', {'class': 'weather-value'}).text)) - 32 ) * (5/9)
        try:
            data['workout_location'] = activity_soup.find('span', {'class':'location'}).text
        except:
            pass

        tr = activity_soup.find_all("tr")
        tr_datas = BeautifulSoup(str(tr), "html.parser").get_text()
        tr_datas = tr_datas.strip('][').split(', ')[1:]
        tr_datas = list(map(lambda x: x.split('\n'), tr_datas))
        tr_datas = list(map(lambda dt: [x for x in dt if x], tr_datas))

        tr_dict = {}

        for dt in tr_datas:

            name = dt[0]
            try:
                if name == 'Speed':

                    tr_dict['speed_average'] = float(dt[1][:-4].replace(',', ''))
                    tr_dict['speed_maximum'] = float(dt[2][:-4].replace(',', ''))

                elif name == 'Heart Rate':
                    tr_dict['hr_average'] = float(dt[1][:-3].replace(',', ''))
                    tr_dict['hr_maximum'] = float(dt[2][:-3].replace(',', ''))

                elif name == 'Calories':
                    tr_dict['calories'] = float(dt[1].replace(',', ''))

                elif name == 'Cadence':
                    tr_dict['cadence_average'] = float(dt[1].replace(',', ''))
                    tr_dict['cadence_maximum'] = float(dt[2].replace(',', ''))

                elif name == 'Power':
                    tr_dict['power_avg'] = float(dt[1][:-1].replace(',', ''))
                    tr_dict['power_max'] = float(dt[2][:-1].replace(',', ''))

                elif name == 'Temperature':
                    tr_dict['temp_avg'] = float(dt[1][:-1])

                elif name == 'Elapsed Time':
                    pass
                else:
                    break
            except:
                continue

        if 'calories' in tr_dict.keys():
            data['calories'] = tr_dict['calories']


        data['workout_title'] = activity_soup.find('h1').text

        data['athelete_name'] = activity_soup.find('a', {'class':'minimal'}).text

        analysis_exists = False
        zone_distribution_exists = False
        heart_rate_exists = False
        try:
            site_menu = activity_soup.find('ul', {'class': 'pagenav'}).find_all('a')
        except:
            site_menu = []

        for a in site_menu:
            if a['data-menu'] == 'analysis':
                analysis_exists = True

        try:
            premium_views = activity_soup.find('li', {'id': 'premium-views'}).find_all('a')
        except:
            premium_views = []
        for a in premium_views:
            if a['data-menu'] == 'heartrate':
                heart_rate_exists = True

            if a['data-menu'] == 'zone-distribution':
                zone_distribution_exists = True

        return data, analysis_exists, zone_distribution_exists, heart_rate_exists

    def _extract_activity_analysis(self, url):

        
        data = {}
        
        t.sleep(0.5)
        curr_url = url + '/analysis'
        self.browser.get(curr_url)

        self._check_if_too_many_requests(curr_url)
        
        
        #     print(browser.current_url)
        try:
            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            chart = analysis_soup.find_all('g', {'class': "label-box"})
            svg = analysis_soup.find_all('defs')
            before = t.time()
            dead_line = 5
            timeout = t.time() + dead_line
            too_much = t.time() + 50
            while len(chart) == 0 or len(svg) == 0: # Wait for load
                analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                chart = analysis_soup.find_all('g', {'class': "label-box"})
                svg = analysis_soup.find_all('defs')
                if t.time() > too_much:
                    return {}
                elif t.time() > timeout:
                    log('did not load analysis graphs. SWITCHING ACCOUNT', 'WARNING', id=self.id)
                    self._switchAccount(curr_url)
                    timeout = t.time() + dead_line

                t.sleep(0.1)
            after = t.time() - before
            print(f'loaded: {after}')


            # Raw data (speed, est power, heart rate)
            for label_box in chart:
                text_data = []
                for text in label_box.find_all('text'):
                    text_data.append(text.get_text())

                name = text_data[0].lower().replace(' ', '_')
                max_attribute = text_data[1].split(' ')[1]
                avg_attribute = text_data[2].split(' ')[1]

                if name == 'heart_rate':
                    name = 'hr'

                elif name == 'temperature':
                    name = 'temp'

                data[f'{name}_maximum'] = max_attribute
                data[f'{name}_average'] = avg_attribute

            e_g_e_d = extract_graph_elevation_distance(analysis_soup)
            data.update(e_g_e_d)

            button = self.browser.find_element_by_css_selector("g[data-type='time']")

            button.click()

            timeout = t.time() + 5
            loading = True
            while loading:
                t.sleep(0.1)

                analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                axis = analysis_soup.find('g', {'class':'axis xaxis'})
                tick = axis.find_all('g', {'class': 'tick'})[1]

                try:
                    time = list(reversed(tick.find('text').text.replace('s', '').split(':')))[0]
                    int(time)
                    loading = False
                except Exception as e:
                    if t.time() > timeout:
                        print('didnt load analysis metrics', e, url + '/analysis')
                        break
                    button = self.browser.find_element_by_css_selector("g[data-type='time']")
                    button.click()

            if not loading:
                analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                e_m_m_m = extract_mean_max_metrics(analysis_soup)
                data.update(e_m_m_m)
            
                
        except Exception as e:
            log(f'BAD LINK: | {curr_url} | {e}', 'WARNING', id=self.id)

        return data

    def _extract_activity_zones_distribution(self, url, zones_distribution_exist, heart_rate_exists):
        url_extensions = ['/zone-distribution', '/heartrate']
        prefixes = ['power', 'hr']
        data = {}
        j = 0
        for extension in url_extensions:
            if not (j == 0 and zones_distribution_exist or j == 1 and heart_rate_exists):
                continue

            curr_url = url + extension
            self.browser.get(curr_url)
            t.sleep(0.5)
            self._check_if_too_many_requests(curr_url)

            #         print(browser.current_url)
            try:
                zone_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                zones = zone_soup.find_all('tr')
                while len(zones) is None:
                    zone_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                    zones = zone_soup.find_all('tr')
                    t.sleep(0.1)

                zone_dist_dict = {}

                for zone in zones:
                    z = [x for x in zone.get_text().strip().split('\n') if x]

                    if not z[0].startswith("Z"):
                        continue

                    z_name = z[0]
                    z_min = z[2].split(' ')
                    z_min = [re.sub('[^0-9]', '', x) for x in z_min]
                    z_min = [x for x in z_min if x]
                    z_min = float(z_min[0])

                    z_time = to_seconds(z[-2])
                    zone_dist_dict[f'{prefixes[j]}_{z_name}'.lower()] = z_time
                    zone_dist_dict[f'{prefixes[j]}_{z_name}_min'.lower()] = z_min

                for i in range(1,8):
                    if f'{prefixes[j]}_z{i}' in zone_dist_dict:
                        data[f'{prefixes[j]}_zone_{i}'] = zone_dist_dict[f'{prefixes[j]}_z{i}']
                        data[f'{prefixes[j]}_zone_{i}_min'] = zone_dist_dict[f'{prefixes[j]}_z{i}_min']
                    else:
                        data[f'{prefixes[j]}_zone_{i}'] = None
                        data[f'{prefixes[j]}_zone_{i}_min'] = None

            except Exception as e:
                log(f'BAD LINK: | {curr_url} | {e}', 'WARNING', id=self.id)

            finally:
                j += 1

        return data


    def _rand_sleep(self):
        pass

    def run(self):

        self._open_driver()
        total_links = 0
        for rider in self.riders:
            total_links += len(rider.activity_links)
        i = 1

        for rider in self.riders:
            log(f"WATCHING RIDER: {rider}", id=self.id)
            for link in list(rider.activity_links):
                if not i >= self.start_from_index:
                    i += 1
                    continue
                data = {}
                try:
                    if self.browser.current_url == LOGIN_URL:
                        self._close_driver()
                        self._open_driver()

                    home, analysis_exist, zones_distribution_exist, heart_rate_exists = self._extract_activity_home(link)
                    data.update(home)

                    if analysis_exist:

                        analysis = self._extract_activity_analysis(link)
                        data.update(analysis)

                    zones_distribution = self._extract_activity_zones_distribution(link, zones_distribution_exist, heart_rate_exists)
                    data.update(zones_distribution)

                    workout_row, workout_hrs_row, workout_cadences_row, workout_powers_row, workout_speeds_row, key_not_found = divide_to_tables(data, rider.rider_id)
                    try:
                        append_row_to_csv(self.saving_file_name+'_workout', workout_row, workout_columns)
                        append_row_to_csv(self.saving_file_name+'_workout_hrs', workout_hrs_row, workout_hrs_columns)
                        append_row_to_csv(self.saving_file_name+'_workout_cadences', workout_cadences_row, workout_cadences_columns)
                        append_row_to_csv(self.saving_file_name+'_workout_powers', workout_powers_row, workout_powers_columns)
                        append_row_to_csv(self.saving_file_name+'_workout_speeds', workout_speeds_row, workout_speeds_columns)
                    except Exception as e:
                        log(f'could not save locally {e}', 'ERROR', id=self.id)

                    rider.workout.append(workout_row)
                    rider.workout_hrs.append(workout_hrs_row)
                    rider.workout_cadences.append(workout_cadences_row)
                    rider.workout_powers.append(workout_powers_row)
                    rider.workout_speeds.append(workout_speeds_row)
                    msg = f'{i} / {total_links}, {link}'

                    log(msg, id=self.id)

                except Exception as e:
                    log(f'{i} / {total_links}, BAD LINK: | {link} | {e}', 'ERROR', id=self.id)
                    self._restart_browser()
                    # if 'invalid session id' in f'{e}':
                    #     self._switchAccount(link)

                finally:
                    i += 1

                    t.sleep(2)

        self._close_driver()





