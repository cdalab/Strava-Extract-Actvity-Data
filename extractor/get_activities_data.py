import time as t
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from utils import *


STRAVA_URL = 'https://www.strava.com'






class Get_Activities_Data:

    def __init__(self, username, riders, id):
        self.username = username
        self.riders = riders
        self.id = id
        self.STRAVA_URL = 'https://www.strava.com'


    def _log(self, msg,level='INFO'):

        try:
            msg=f"{level} {datetime.now()} {msg}\n"
            print(f'{msg}')
            with open(f"log_{self.id}.txt",'a+') as f:
                f.write(msg)
            with open(f"S:/log_{self.id}.txt",'a+') as f:
                f.write(msg)
        except Exception as err:
            pass


    def _open_driver(self):

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        self.browser = webdriver.Chrome(options=options)
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

    def _is_logged_out(self):
        site_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        if site_soup.find('html')['class'][0] == 'logged-out': # logged out ...
            self._log("Logged out...")
            #print(f'logged out...')
            return True
        return False

    def _extract_activity_home(self, url):
        data = {}
        self.browser.get(url)
        t.sleep(0.2)
        # print(self.browser.current_url)

        activity_soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        data['type'] = activity_soup.find('span', {'class': 'title'}).text.split('\n')[-2]
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
            data['distance'] = float(strong_dict['distance'][:-2])*1609.34
        else:
            data['distance'] = None

        if 'moving time' in strong_dict.keys():
            time = strong_dict['moving time'].split(':')
            total_time = 0
            for i in range(len(time)):
                total_time += int(re.sub("[^0-9]", "", time[i]))/(60**i)
            data['total_time'] = total_time
        else:
            data['total_time'] = None

        if 'relative effort' in strong_dict.keys():
            data['relative_effort'] = float(strong_dict['relative effort'])
        else:
            data['relative_effort'] = None

        if 'total work' in strong_dict.keys():
            data['energy'] = float(strong_dict['total work'][:-2].replace(',', ''))
        else:
            data['energy'] = None

        if 'training load' in strong_dict.keys():
            data['training_load'] = float(strong_dict['training load'])
        else:
            data['training_load'] = None

        if 'intensity' in strong_dict.keys():
            data['intensity'] = float(strong_dict['intensity'][:-1])
        else:
            data['intensity'] = None

        if 'relative effort' in strong_dict.keys():
            data['relative_effort'] = float(strong_dict['relative effort'])
        else:
            data['relative_effort'] = None

        date = activity_soup.find('time').text.replace('\n', '')
        date = datetime.strptime(date, '%A, %B %d, %Y')
        data['workout_datetime'] = date
        data['workout_week'] = date.isocalendar()[1]
        data['workout_month'] = date.month
        #data['temp_avg'] = (float(re.sub('\D', '', activity_soup.find('div', {'class': 'weather-value'}).text)) - 32 ) * (5/9)

        tr = activity_soup.find_all("tr")
        tr_datas = BeautifulSoup(str(tr), "html.parser").get_text()
        tr_datas = tr_datas.strip('][').split(', ')[1:]
        tr_datas = list(map(lambda x:x.split('\n'), tr_datas))
        tr_datas = list(map(lambda dt :[x for x in dt if x], tr_datas))

        tr_dict = {}

        for dt in tr_datas:

            name = dt[0]

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

        data['temp_min'] = None
        data['temp_max'] = None

        if 'calories' in tr_dict.keys():
            data['calories'] = tr_dict['calories']
        else:
            data['calories'] = None

        data['workout_title'] = activity_soup.find('h1').text
        data['athelete_name'] = activity_soup.find('a', {'class':'minimal'}).text
        data['normalized_power'] = None
        data['IF'] = None
        data['tss_actual'] = None
        data['tss_calculation_method'] = None
        data['hidden'] = None
        data['locked'] = None

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
        self.browser.get(url + '/analysis')
        #     print(browser.current_url)
        t.sleep(0.2)
        analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        chart = analysis_soup.find_all('g', {'class': "label-box"})
        svg = analysis_soup.find_all('defs')

        timeout = t.time() + 3
        while len(chart) == 0 or len(svg) == 0: # Wait for load
            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            chart = analysis_soup.find_all('g', {'class': "label-box"})
            svg = analysis_soup.find_all('defs')
            if t.time() > timeout:
                return {}
            t.sleep(0.5)

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
        t.sleep(0.2)

        timeout = t.time() + 5
        loading = True
        while loading:
            t.sleep(0.5)

            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            axis = analysis_soup.find('g', {'class':'axis xaxis'})
            tick = axis.find_all('g', {'class': 'tick'})[1]
            time = list(reversed(tick.find('text').text.replace('s', '').split(':')))[0]

            try:
                int(time)
                loading = False
            except:
                if t.time() > timeout:
                    break

        if not loading:
            analysis_soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            e_m_m_m = extract_mean_max_metrics(analysis_soup)
            data.update(e_m_m_m)
        return data

    def _extract_activity_zones_distribution(self, url, zones_distribution_exist, heart_rate_exists):
        url_extensions = ['/zone-distribution', '/heartrate']
        prefixes = ['power', 'hr']
        data = {}
        j = 0
        for extension in url_extensions:
            if not (j == 0 and zones_distribution_exist or j == 1 and heart_rate_exists):
                continue
            self.browser.get(url + extension)
            #         print(browser.current_url)
            t.sleep(0.2)
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
            j += 1

        return data

    def run(self):
        self._open_driver()

        total_links = 0
        for rider in self.riders:
            total_links += len(rider.activity_links)
        i = 1
        for rider in self.riders:

            for link in rider.activity_links:
                t.sleep(0.5)
                data = {}

                if not self._is_logged_out():
                    home, analysis_exist, zones_distribution_exist, heart_rate_exists = self._extract_activity_home(link)
                    data.update(home)
                    try:
                        if analysis_exist:
                            analysis = self._extract_activity_analysis(link)
                            data.update(analysis)

                        zones_distribution = self._extract_activity_zones_distribution(link, zones_distribution_exist, heart_rate_exists)
                        data.update(zones_distribution)

                        workout_row, workout_hrs_row, workout_cadences_row, workout_powers_row, workout_speeds_row, key_not_found = divide_to_tables(data, rider.rider_id)
                        rider.workout.append(workout_row)
                        rider.workout_hrs.append(workout_hrs_row)
                        rider.workout_cadences.append(workout_cadences_row)
                        rider.workout_powers.append(workout_powers_row)
                        rider.workout_speeds.append(workout_speeds_row)
                        msg = f'{i} / {total_links}, {link}'

                        self._log(msg)


                        i += 1
                    except:
                        self._log(f'BAD LINK: {link}', 'ERROR')
                       # print(f'BAD LINK: {link}')
                        continue
                else:
                    self._close_driver()
                    return

        self._close_driver()





