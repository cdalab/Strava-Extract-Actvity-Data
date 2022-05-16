import json
import os.path
from urllib.parse import parse_qsl
import shutil
import pandas as pd
from bs4 import BeautifulSoup
from utils import *
from Browser import Browser


class DataExtractor(Browser):

    def __init__(self, id, pages, html_files_path):
        Browser.__init__(self, id)
        self.pages = pages
        self.html_files_path = html_files_path
        Path(f'link/{self.id}').mkdir(parents=True, exist_ok=True)
        self.overview_data_path = f'data/{self.id}/overview_data.csv'
        self.main_page_handler_path = f'link/{self.id}/processed_rider_main_page_files.txt'
        self.year_time_interval_handler_path = f'link/{self.id}/processed_year_intervals_files.txt'
        self.week_time_interval_handler_path = f'link/{self.id}/processed_week_intervals_files.txt'
        self.activity_handler_path = f'link/{self.id}/processed_activity_files.txt'
        self.analysis_pages_handler_path = f'link/{self.id}/processed_analysis_files.txt'
        self.download_again_file_path = f'link/{self.id}/links_to_download_again.csv'
        self.time_interval_handlers_paths = [self.main_page_handler_path, self.year_time_interval_handler_path,
                                             self.week_time_interval_handler_path]

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        html_file_name = "_".join(url_param_dict.values())
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    def _fetch_rider_year_interval_links(self, rider_id, csv_file_path, global_csv_file_path, start_year, start_week,
                                         end_week):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            for rider_html_file in os.listdir(rider_dir_path):
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', self.main_page_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', MAIN_PAGE_HANDLER_PATH):
                    continue
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', self.year_time_interval_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', YEAR_TIME_INTERVAL_HANDLER_PATH):
                    continue
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', self.week_time_interval_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{rider_html_file}', WEEK_TIME_INTERVAL_HANDLER_PATH):
                    continue
                html_content = read_from_html(rider_dir_path, rider_html_file)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                options_soup = rider_soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
                option_list = options_soup.find('ul', 'options').find_all('a')
                for time_interval in option_list:
                    self._handle_time_interval_page(rider_id, time_interval, csv_file_path, global_csv_file_path,
                                                    start_year, start_week,
                                                    end_week)
                write_to_file_handler(f'{rider_dir_path}/{rider_html_file}', self.main_page_handler_path)

        except:
            log(f'Could not fetch year interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_year_interval_links(self, csv_file_path, global_csv_file_path, start_year, start_week, end_week):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching year interval links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._fetch_rider_year_interval_links(rider_id, csv_file_path, global_csv_file_path, start_year,
                                                      start_week, end_week)
                i += 1
        except:
            log(f'Failed fetching riders year interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _handle_time_interval_page(self, rider_id, interval, csv_file_path, global_csv_file_path, start_year,
                                   start_week, end_week):
        link = f"{BASE_STRAVA_URL}{interval.attrs['href']}"
        csv_exists = os.path.exists(csv_file_path)
        if csv_exists and (link in list(pd.read_csv(csv_file_path)['time_interval_link'].values)):
            return
        global_csv_exists = os.path.exists(global_csv_file_path)
        if global_csv_exists and (link in list(pd.read_csv(global_csv_file_path)['time_interval_link'].values)):
            return
        url_param_dict = dict(parse_qsl(link.split('?')[1]))
        interval = url_param_dict['interval']
        curr_year, curr_week = int(interval[:4]), int(interval[4:])
        if (start_year is not None) and (curr_year < start_year):
            return
        if start_week is not None:
            start_year, s_week = int(start_week[:4]), int(start_week[4:])
            if (curr_year < start_year) or (curr_week < s_week):
                return
        if end_week is not None:
            end_year, e_week = int(end_week[:4]), int(end_week[4:])
            if (curr_year >= end_year) or (curr_week >= e_week):
                return
        row = {'rider_id': rider_id,
               'time_interval_link': link}
        append_row_to_csv(csv_file_path, row)

    def _fetch_rider_week_interval_links(self, rider_id, csv_file_path, global_csv_file_path, start_year, start_week,
                                         end_week):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_year_interval_files = os.listdir(rider_dir_path)
            i = 0
            for year_interval_file in rider_year_interval_files:
                if is_file_handled(f'{rider_dir_path}/{year_interval_file}', self.year_time_interval_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{year_interval_file}', YEAR_TIME_INTERVAL_HANDLER_PATH):
                    continue
                if is_file_handled(f'{rider_dir_path}/{year_interval_file}', self.week_time_interval_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{year_interval_file}', WEEK_TIME_INTERVAL_HANDLER_PATH):
                    continue
                log(f'Fetching week interval links from file {year_interval_file}, {i} / {len(rider_year_interval_files) - 1}',
                    id=self.id, debug=False)
                html_content = read_from_html(rider_dir_path, year_interval_file)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                rider_intervals = rider_soup.find('ul', attrs={'class': 'intervals'}).find_all('a')
                for week_interval in rider_intervals:
                    self._handle_time_interval_page(rider_id, week_interval, csv_file_path, global_csv_file_path,
                                                    start_year, start_week,
                                                    end_week)

                write_to_file_handler(f'{rider_dir_path}/{year_interval_file}', self.year_time_interval_handler_path)
                print_progress_bar(i + 1, len(rider_year_interval_files), prefix='Progress:', suffix='Complete',
                                   length=50)
                i += 1
        except:
            log(f'Could not fetch week interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_week_interval_links(self, csv_file_path, global_csv_file_path, start_year, start_week, end_week):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching week interval links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._fetch_rider_week_interval_links(rider_id, csv_file_path, global_csv_file_path, start_year,
                                                      start_week, end_week)
                i += 1
        except:
            log(f'Failed fetching riders week interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_activity_links(self, rider_id, csv_file_path, global_csv_file_path, start_year):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_week_interval_files = os.listdir(rider_dir_path)
            i = 0
            for week_interval_file in rider_week_interval_files:
                curr_year = int(week_interval_file[:4])
                if (start_year is not None) and (curr_year < start_year):
                    continue
                if is_file_handled(f'{rider_dir_path}/{week_interval_file}', self.week_time_interval_handler_path):
                    continue
                if is_file_handled(f'{rider_dir_path}/{week_interval_file}', WEEK_TIME_INTERVAL_HANDLER_PATH):
                    continue
                log(f'Fetching activity links from file {week_interval_file}, {i} / {len(rider_week_interval_files) - 1}',
                    id=self.id, debug=False)
                html_content = read_from_html(rider_dir_path, week_interval_file)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                activities_feed_container = rider_soup.select('div[id="interval-rides"]')[0]
                old_structure_container = activities_feed_container.select('div[class="feed"]')
                if len(old_structure_container) > 0:
                    activities_soup = old_structure_container[0]
                    self.handle_activities_extraction_old_structure(activities_soup, csv_file_path,
                                                                    global_csv_file_path, rider_id,
                                                                    week_interval_file)
                else:
                    new_structure_container = activities_feed_container.select('div[class*="feed-component"]')
                    activities_soup = new_structure_container[0]
                    self.handle_activities_extraction_new_structure(activities_soup, csv_file_path,
                                                                    global_csv_file_path, rider_id)

                write_to_file_handler(f'{rider_dir_path}/{week_interval_file}',
                                      self.week_time_interval_handler_path)
                print_progress_bar(i + 1, len(rider_week_interval_files), prefix='Progress:', suffix='Complete',
                                   length=50)
                i += 1

        except:
            log(f'Could not fetch time interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def handle_activities_extraction_old_structure(self, activities_soup, csv_file_path, global_csv_file_path, rider_id,
                                                   week_interval_file):
        activities_list = activities_soup.find_all('div', attrs={
            'class': 'react-card-container'})
        for activity_card in activities_list:
            a_type = activity_card.find(
                lambda tag: (tag.name == 'div') and ('data-react-class' in tag.attrs))
            if a_type['data-react-class'] not in ACTIVITY_POST_TYPES:
                log(f"New post activity type found: {a_type['data-react-class']}", 'WARNING', id=self.id)
            activity_a = activity_card.find_all(
                lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
            if len(activity_a) > 0:
                if a_type['data-react-class'] != 'GroupActivity':
                    activity_a = activity_a[0]
                else:
                    entries = activity_card.find(
                        lambda tag: (tag.name == 'ul') and ('class' in tag.attrs) and (
                                'GroupActivity--list-entries' in str(tag.attrs['class'])))
                    for entry in entries.contents:
                        link = entry.find(lambda tag: tag.name == 'a' and (
                                ('athletes' in tag.attrs['href']) or ('pros' in tag.attrs['href'])))['href']
                        if float(link.split('/')[-1]) == float(rider_id):
                            activity_a = entry.find(
                                lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
                            break
                activity_link = f"{BASE_STRAVA_URL}{activity_a.attrs['href']}"
                csv_exists = os.path.exists(csv_file_path)
                if csv_exists and (
                        activity_link in list(pd.read_csv(csv_file_path)['activity_link'].values)):
                    continue
                activity_id = activity_link.split('/activities/')[1]
                self.write_activity(activity_link, activity_id, csv_file_path, global_csv_file_path, rider_id)

            else:
                if activity_card.find('div', attrs={'data-react-class': "Activity"}) is not None:
                    raise ValueError(
                        f'Activity missed and should be recognized, interval file {week_interval_file}')
                challenge = activity_card.find('div', attrs={'data-react-class': 'ChallengeJoin'})
                join_club = activity_card.find('div', attrs={'data-react-class': "ClubJoin"})
                if (challenge is None) and (join_club is None):
                    raise ValueError(
                        f'Activity card type is not recognized, interval file {week_interval_file}')

    def write_activity(self, activity_link, activity_id, csv_file_path, global_csv_file_path, rider_id):
        activity_not_extracted = (not os.path.exists(csv_file_path))
        if not activity_not_extracted:
            local_csv = pd.read_csv(csv_file_path)
            activity_record_in_csv = local_csv[
                (local_csv['activity_id'] == float(activity_id)) & (local_csv['rider_id'] == float(rider_id))]
            activity_not_extracted = activity_not_extracted or activity_record_in_csv.empty
            activity_not_extracted = activity_not_extracted or (not os.path.exists(global_csv_file_path))
        if not activity_not_extracted:
            global_csv = pd.read_csv(global_csv_file_path)
            activity_record_in_csv = global_csv[
                (global_csv['activity_id'] == float(activity_id)) & (global_csv['rider_id'] == float(rider_id))]
            activity_not_extracted = activity_not_extracted or activity_record_in_csv.empty
        if activity_not_extracted:
            row = {'rider_id': rider_id,
                   'activity_link': activity_link,
                   'activity_id': activity_id}
            append_row_to_csv(csv_file_path, row)

    def handle_activities_extraction_new_structure(self, activities_soup, csv_file_path, global_csv_file_path,
                                                   rider_id):
        activities_list = activities_soup.select('div[class*="Feed"]')
        activities_meta_data = json.loads(activities_soup['data-react-props'])['preFetchedEntries']
        for i in range(len(activities_list)):
            activity_meta_data = activities_meta_data[i]
            activity_type = activity_meta_data['entity']
            if activity_type not in ACTIVITY_POST_TYPES:
                log(f"New post activity type found: {activity_type}", 'WARNING', id=self.id)
            if activity_type == 'Activity':
                activity_id = activity_meta_data['activity']['id']
            elif activity_type == 'GroupActivity':
                group_activities_data = activity_meta_data['rowData']['activities']
                activity_id = [a for a in group_activities_data if float(a['athlete_id']) == float(rider_id)][0][
                    'activity_id']
            else:
                return
            activity_link = f"{BASE_STRAVA_URL}/activities/{activity_id}"
            self.write_activity(activity_link, activity_id, csv_file_path, global_csv_file_path, rider_id)

    def extract_rider_activity_links(self, csv_file_path, global_csv_file_path, start_year):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching activity links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._fetch_rider_activity_links(rider_id, csv_file_path, global_csv_file_path, start_year)
                i += 1

        except:
            log(f'Failed fetching rider activity links, current rider fetched {rider_id}', 'ERROR',
                id=self.id)

    def _validate_activity_page(self, activity_soup, rider_id, activity_id):
        heading = activity_soup.find('section', attrs={'id': 'heading'})
        rider_in_page = heading.find(
            lambda tag: (tag.name == "a") and (
                    ("/athletes/" in tag.attrs['href']) or ("/pros/" in tag.attrs['href'])))
        rider_href = rider_in_page['href']
        rider_in_page = float(rider_href.split('/')[-1]) if check_int(rider_href.split('/')[-1]) else None
        if (rider_in_page is None) or (rider_in_page != float(rider_id)):
            raise ValueError(
                f'The cyclist {rider_id} mapped to activity {activity_id}, but the real rider for this activity is {rider_in_page}')
        units_in_page = [u['title'] for u in heading.find_all('abbr', attrs={'class': 'unit'})]
        if any([unit in units_in_page for unit in UNDESIRED_UNITS]):
            raise ValueError(
                f'The metrics in the page of activity {activity_id}, cyclist {rider_id}, are wrong.')
        if 'Ride' not in activity_soup.find('head').find('title').text:
            raise ValueError(
                f'The activity should be Ride- id {activity_id}, cyclist {rider_id}.')

    def _activity_analysis_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_activity_files = os.listdir(rider_dir_path)
            i = 0
            for activity_id in rider_activity_files:
                log(f"Fetching activity analysis from file {rider_dir_path}/{activity_id}/overview.html, {i} / {len(rider_activity_files) - 1}",
                    id=self.id, debug=False)
                html_content = read_from_html(f"{rider_dir_path}/{activity_id}", 'overview.html')
                activity_soup = BeautifulSoup(html_content, 'html.parser')
                title = activity_soup.find('section', attrs={'id': 'heading'}).find('span', attrs={
                    'class': 'title'}).text.replace('\n', '')
                deli_idx = title.find('–')
                activity_type = title[deli_idx + 1:].strip() if deli_idx > 0 else None
                if activity_type not in ACTIVITY_TYPES:
                    log(f"New activity type found: {activity_type}", 'WARNING', id=self.id)
                menu_options = activity_soup.find('nav', attrs={'class': 'sidenav'}).find_all('a')
                self._validate_activity_page(activity_soup, rider_id, activity_id)
                for option in menu_options:
                    ref = option.attrs['href']
                    activity_option_link = f"{BASE_STRAVA_URL}{ref}"
                    option_type = ref.split(f"{activity_id}")[-1]
                    csv_exist = os.path.exists(csv_file_path)
                    if (option_type in OPTIONS_TO_IGNORE) or (csv_exist and (
                            activity_option_link in list(pd.read_csv(csv_file_path)['activity_option_link'].values))):
                        continue
                    if option_type not in ANALYSIS_PAGE_TYPES:
                        log(f"New activity analysis type found: {option_type}", 'WARNING', id=self.id)
                    row = {'rider_id': rider_id,
                           'activity_id': activity_id,
                           'activity_option_link': activity_option_link,
                           'option_type': option_type,
                           'activity_type': activity_type}
                    append_row_to_csv(csv_file_path, row)
                print_progress_bar(i + 1, len(rider_activity_files), prefix='Progress:', suffix='Complete',
                                   length=50)
                i += 1
        except:
            log(f'Could not fetch analysis links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_activity_analysis_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching activity analysis links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._activity_analysis_links(rider_id, csv_file_path)
                i += 1

        except:
            log(f'Failed fetching rider activity links, current rider fetched {rider_id}', 'ERROR',
                id=self.id)

    def _fetch_activity_analysis_data(self, rider_id, data_types):
        try:
            processed_files = set()
            if os.path.exists(self.analysis_pages_handler_path):
                with open(self.analysis_pages_handler_path) as f:
                    processed_files = set(f.readlines())
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_activity_dirs = os.listdir(rider_dir_path)
            i = 0
            for activity_id in rider_activity_dirs:
                log(f"Fetching activity data from {rider_dir_path}/{activity_id}, {i} / {len(rider_activity_dirs) - 1}",
                    id=self.id, debug=False)
                activity_dir_path = f"{rider_dir_path}/{activity_id}"
                rider_activity_files = os.listdir(activity_dir_path)
                for activity_file in rider_activity_files:
                    if f'{activity_dir_path}/{activity_file}\n' in processed_files:
                        continue
                    if os.path.isdir(f"{activity_dir_path}/{activity_file}"):
                        continue
                    activity_link = f"{BASE_STRAVA_URL}/activities/{activity_id}"
                    html_content = read_from_html(activity_dir_path, activity_file)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    title = soup.find('section', attrs={'id': 'heading'}).find('span', attrs={
                        'class': 'title'}).text.strip()
                    deli_idx = title.find('–')
                    activity_type = title[deli_idx + 1:].strip() if deli_idx > 0 else None
                    if (data_types is not None) and all([f not in activity_file for f in data_types]):
                        continue
                    if 'overview' in activity_file:
                        activity_link += '/overview'
                        args = (activity_file, activity_link, rider_id, activity_id, activity_type)
                        self._handle_overview_page(soup, *args)
                    elif 'analysis' in activity_file:
                        activity_link += '/analysis'
                        args = (activity_file, activity_link, rider_id, activity_id, activity_type)
                        self._handle_analysis_page(soup, *args)
                    elif 'power-curve' in activity_file:
                        activity_link += '/power-curve' if 'est' not in activity_file else '/est-power-curve'
                        args = (activity_file, activity_link, rider_id, activity_id, activity_type)
                        self._handle_power_curve_page(soup, *args)
                    elif ('heartrate' in activity_file) or ('zone' in activity_file):
                        activity_link += '/heartrate' if 'heartrate' in activity_file else '/zone-distribution'
                        args = (activity_file, activity_link, rider_id, activity_id, activity_type)
                        self._handle_table_page(soup, *args)
                    elif 'power-distribution' in activity_file:
                        activity_link += '/power-distribution' if 'est' not in activity_file else '/est-power-distribution'
                        args = (activity_file, activity_link, rider_id, activity_id, activity_type)
                        self._handle_power_distribution_page(soup, *args)
                    elif all([f[1:] not in activity_file for f in ANALYSIS_PAGE_TYPES]):
                        log(f'Could not fetch analysis data for activity file {rider_dir_path}/{activity_id}/{activity_file}, unknown type page.',
                            'ERROR', id=self.id)
                print_progress_bar(i + 1, len(rider_activity_dirs), prefix='Progress:', suffix='Complete',
                                   length=50)
                i += 1
        except:
            log(f'Could not fetch analysis data for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_data_from_analysis_activities(self, data_types):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching activity analysis data for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._fetch_activity_analysis_data(rider_id, data_types)
                i += 1

        except:
            log(f'Failed fetching rider activity links, current rider fetched {rider_id}', 'ERROR',
                id=self.id)

    def _handle_overview_ul_table(self, activity_id, rider_id, ul_table, data, args):
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - overview table li's missing."
        for ul in ul_table:
            lis = ul.find_all('li')
            if self._element_doesnt_exists(((len(ul.contents) == 0) or (len(lis) == 0)), warn_msg, *args):
                return
            for li in lis:
                if li.find('strong').find('a') is None:
                    value = li.find('strong').contents[0].text.replace(',', '').replace('%', '')
                else:
                    value = li.find('strong').find('a').text.strip()
                label = li.find('div').text.strip()
                if '—' in value:
                    continue
                if any([(l in label.lower()) for l in ['time', 'duration']]):
                    value = string_to_time(value)
                try:
                    value = float(value)
                    data[label] = value
                except Exception as err:
                    raise ValueError(f'Cannot parse li - label {label}, {err}')
        return data

    def _handle_overview_div(self, activity_id, rider_id, div_table, data, args):
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - overview table div's contents missing."
        for div in div_table:
            if self._element_doesnt_exists((len(div.contents) == 0), warn_msg, *args):
                return
            table = div.find('table')
            device = div.find('div', attrs={'class': 'device spans8'})
            weather_div = div.select('div[class*="weather"]')
            if table is not None:
                theads = table.find('thead').find_all('th')
                for tr in table.find_all('tr')[1:]:
                    j = 0
                    label_suffix, label, value = '', '', ''
                    for c in tr.findChildren(recursive=False):
                        if c.name == 'th':
                            label_suffix = c.text
                        elif c.name == 'td':
                            for ch in c.findChildren(recursive=False):
                                if (ch.name == 'abbr') and (any([unit in ch['title'] for unit in UNDESIRED_UNITS])):
                                    raise ValueError(
                                        f'The metrics in the page of activity {activity_id}, cyclist {rider_id}, are wrong.')
                            if 'colspan' in c.attrs:
                                if j != 1:
                                    print('not expected')
                                else:
                                    label = label_suffix.strip()
                            else:
                                label = f'{theads[j].text}{label_suffix}'
                            value = c.contents[0].text.replace(',', '').strip()
                            if '—' in value:
                                continue
                            if any([(l in label.lower()) for l in ['time', 'duration']]):
                                value = string_to_time(value)
                            try:
                                value = float(value)
                                data[label] = value
                            except Exception as err:
                                raise ValueError(f'Cannot parse tr - label {label}, {err}')
                        else:
                            raise ValueError(
                                f'Unknown structure in the overview page of activity {activity_id}, cyclist {rider_id}, are wrong.')
                        j += 1
            elif device is not None:
                data["Device"] = div.find('div').find('div').text.strip() if all(
                    [e is not None for e in [div.find('div'), div.find('div').find('div')]]) else None
            elif 'Perceived Exertion' in div.text:
                data["Perceived Exertion"] = div.find('span').text
            elif len(weather_div) != 0:
                stats = div.select('div[class="weather-stat"]')
                for stat in stats:
                    label, value = stat.find('div', attrs={'class': 'weather-label'}).text.strip(), stat.find('div',
                                                                                                              attrs={
                                                                                                                  'class': 'weather-value'})
                    if value is not None:
                        data[label] = value.text.split()[0].strip()
                    else:
                        data['Weather'] = label

            else:
                raise ValueError(f"Unfamiliar div type, activity {activity_id}, cyclist {rider_id}")
        return data

    def _handle_overview_table(self, overview_soup, data, file, activity_link, rider_id, activity_id, activity_type):
        args = (file, activity_link, rider_id, activity_id, activity_type)
        overview_table = overview_soup.find('div', attrs={'class': 'spans8 activity-stats mt-md mb-md'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - overview table is empty or doesn't exist."
        if self._element_doesnt_exists(((overview_table is None) or (len(overview_table.contents) == 0)), warn_msg,
                                       *args):
            return
        ul_table = overview_table.find_all('ul')
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - overview table ul's missing."
        if self._element_doesnt_exists((len(ul_table) == 0), warn_msg, *args):
            return
        data = self._handle_overview_ul_table(activity_id, rider_id, ul_table, data, args)

        div_table = overview_table.findChildren("div", recursive=False)
        # warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - overview table div's missing."
        # if self._element_doesnt_exist((len(div_table) == 0), warn_msg, *args):
        #     return
        data = self._handle_overview_div(activity_id, rider_id, div_table, data, args)
        return data

    def _handle_date_and_location(self, overview_soup, data, file, activity_link, rider_id, activity_id, activity_type):
        args = (file, activity_link, rider_id, activity_id, activity_type)
        overview_details_container = overview_soup.find('div', attrs={'class': 'spans8 activity-summary mt-md mb-md'})
        overview_details = overview_details_container.find('div', attrs={'class': 'details'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - date and location don't exist."
        if self._element_doesnt_exists(((overview_details is None) or (len(overview_details.contents) == 0)), warn_msg,
                                       *args):
            return
        data['Date'] = overview_details.find('time').text.strip() if overview_details.find('time') is not None else None
        location = overview_details.find('span', attrs={'class': 'location'})
        data['Location'] = location.text.strip() if location is not None else None
        workout_title = overview_details.find('h1')
        data['Title'] = workout_title.text.strip() if workout_title is not None else None
        return data

    def _handle_overview_page(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        try:
            args = (file, activity_link, rider_id, activity_id, activity_type)
            csv_path = self.overview_data_path
            csv_exists = os.path.exists(csv_path)
            if csv_exists and (activity_id in list(pd.read_csv(csv_path)['activity_id'].values)):
                return
            global_csv_exists = os.path.exists(OVERVIEW_DATA_PATH)
            if global_csv_exists and (activity_id in list(pd.read_csv(OVERVIEW_DATA_PATH)['activity_id'].values)):
                return
            data = {}
            data = self._handle_date_and_location(soup, data, *args)
            data = self._handle_overview_table(soup, data, *args) if data is not None else None
            data['activity_type'] = activity_type
            if data is not None:
                data = json.dumps(data)
                append_row_to_csv(csv_path, {'rider_id': rider_id, 'activity_id': activity_id, 'data': data},
                                  # TODO checking activity_type added to data
                                  columns=['rider_id', 'activity_id', 'data'])
                with open(self.analysis_pages_handler_path, 'a+') as f:
                    file_path = f"{self.html_files_path}/{rider_id}/{activity_id}/{file}"
                    f.write(f'{file_path}\n')
            if activity_type == 'Indoor Cycling':
                self._handle_analysis_stacked_chart(soup, *args)
        except:
            log(f'Failed fetching overview activity data, current rider fetched {rider_id}, activity {activity_id}',
                'ERROR',
                id=self.id)

    def _handle_power_curve_page(self, file, soup, activity_link, rider_id, activity_id):
        pass

    def _section_and_header_handler(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        args = (file, activity_link, rider_id, activity_id, activity_type)
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - section part is missing."
        section = soup.find('div', attrs={'id': 'view'}).find('section', attrs={'class': 'with-border'})
        if self._element_doesnt_exists(((section is None) or (len(section.contents) == 0)), warn_msg, *args):
            return
        header = section.find('header')
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - header is missing."
        if self._element_doesnt_exists(((header is None) or (len(header.contents) == 0)), warn_msg, *args):
            return
        uls_header = header.findChildren('ul')
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - ul's in header are missing."
        if self._element_doesnt_exists(((uls_header is None) or (len(uls_header) == 0)), warn_msg, *args):
            return
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - li's in ul header are missing."
        for ul in uls_header:
            if self._element_doesnt_exists(len(ul.contents) == 0, warn_msg, *args):
                return
        return section

    def _handle_table_page(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        args = (file, activity_link, rider_id, activity_id, activity_type)
        section = self._section_and_header_handler(soup, *args)
        if section is None:
            return
        table = section.find("table")
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - table is missing."
        if self._element_doesnt_exists(((table is None) or (len(table.contents) == 0)), warn_msg, *args):
            return
        tbody = table.find("tbody")
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - tbody is missing."
        if self._element_doesnt_exists(((tbody is None) or (len(tbody.contents) == 0)), warn_msg, *args):
            return
        trs = tbody.findChildren("tr")
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - trs are missing."
        if self._element_doesnt_exists((len(trs) == 0), warn_msg, *args):
            return
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - tds are missing."
        for tr in trs:
            tds = tr.findChildren("td")
            if self._element_doesnt_exists((len(tds) == 0), warn_msg, *args):
                return

    def _handle_power_distribution_page(self, file, soup, activity_link, rider_id, activity_id):
        pass

    def _handle_analysis_page(self, soup, *args):
        self._handle_analysis_stacked_chart(soup, *args)
        self._handle_elevation_chart(soup, *args)

    def _handle_base_chart_and_svg(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        args = (file, activity_link, rider_id, activity_id, activity_type)
        base_chart = soup.find('div', attrs={'class': 'base-chart'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - base chart is missing."
        if self._element_doesnt_exists(((base_chart is None) or (len(base_chart.contents) == 0)), warn_msg, *args):
            return
        svg = base_chart.find('svg')
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - svg is missing."
        if self._element_doesnt_exists(((svg is None) or (len(svg.contents) == 0)), warn_msg, *args):
            return
        return svg

    def _handle_analysis_stacked_chart(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        stacked_chart = soup.find('div', attrs={'id': 'stacked-chart'})
        args = (file, activity_link, rider_id, activity_id, activity_type)
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - stacked chart is missing."
        if self._element_doesnt_exists(stacked_chart is None, warn_msg, *args):
            return
        svg = self._handle_base_chart_and_svg(stacked_chart, *args)
        if svg is None:
            return
        paths = svg.find_all('path', attrs={'class': 'simple-line'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - paths are missing."
        if self._element_doesnt_exists(len(paths) == 0, warn_msg, *args):
            return
        lines = stacked_chart.find_all(lambda tag: (tag.name == 'g') and ('clip-path' in tag.attrs))
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - paths or lines are missing."
        if self._element_doesnt_exists(len(paths) != len(lines), warn_msg, *args):
            return
        boxes = stacked_chart.find_all('g', attrs={'class': 'label-box'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - boxes are missing."
        if self._element_doesnt_exists(len(boxes) != len(paths), warn_msg, *args):
            return

    def _save_activity_page_to_download_again(self, file, activity_link, rider_id, activity_id, activity_type):
        src_dir = f"{self.html_files_path}/{rider_id}/{activity_id}"
        Path(f'{src_dir}/backup').mkdir(parents=True, exist_ok=True)
        shutil.move(f"{src_dir}/{file}", f"{src_dir}/backup/{file}")
        csv_exists = os.path.exists(self.download_again_file_path)
        option_type = activity_link.split(f"{activity_id}")[-1]
        if (not csv_exists) or (
                activity_link not in list(pd.read_csv(self.download_again_file_path)['activity_option_link'].values)):
            activity_to_download = {'rider_id': rider_id,
                                    'activity_id': activity_id,
                                    'activity_option_link': activity_link,
                                    'option_type': option_type,
                                    'activity_type': activity_type}
            append_row_to_csv(self.download_again_file_path, activity_to_download)

    def _handle_elevation_chart(self, soup, file, activity_link, rider_id, activity_id, activity_type):
        elevation_chart = soup.find('div', attrs={'id': 'elevation-chart'})
        args = (file, activity_link, rider_id, activity_id, activity_type)
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - stacked chart is missing."
        if self._element_doesnt_exists(elevation_chart is None, warn_msg, *args):
            return
        svg = self._handle_base_chart_and_svg(elevation_chart, *args)
        if svg is None:
            return
        paths = svg.find_all('path', attrs={'class': 'area-chart-curr'})
        warn_msg = f"Activity {activity_id} of rider {rider_id} should be downloaded again - paths are missing."
        if self._element_doesnt_exists(len(paths) == 0, warn_msg, *args):
            return

    def _element_doesnt_exists(self, pred, msg, *args):
        if pred:
            self._save_activity_page_to_download_again(*args)
            log(msg, "WARNING", id=self.id)
            return True
        return False

    def restore_activities_from_backup(self, data_types=None):
        rider_id = None
        j = 0
        try:
            for rider_id in self.pages:
                log(f'Fetching activity analysis data for cyclist {rider_id}, {j} / {len(self.pages) - 1}',
                    id=self.id)
                rider_dir_path = f"{self.html_files_path}/{rider_id}"
                rider_activity_dirs = os.listdir(rider_dir_path)
                i = 0
                for activity_id in rider_activity_dirs:
                    log(f"Restoring activity page from {rider_dir_path}/{activity_id}, {i} / {len(rider_activity_dirs) - 1}",
                        id=self.id, debug=False)
                    activity_dir_path = f"{rider_dir_path}/{activity_id}"
                    if not os.path.exists(f"{activity_dir_path}/backup"):
                        continue
                    for file in os.listdir(f"{activity_dir_path}/backup"):
                        if (data_types is None) or (any([f in file for f in data_types])):
                            shutil.move(f"{activity_dir_path}/backup/{file}", f"{activity_dir_path}/{file}")
                    if len(os.listdir(f"{activity_dir_path}/backup")) == 0:
                        shutil.rmtree(f"{activity_dir_path}/backup")
                    print_progress_bar(i + 1, len(rider_activity_dirs), prefix='Progress:', suffix='Complete',
                                       length=50)
                    i += 1
                j += 1
        except:
            log(f'Could not restore activity pages for rider {rider_id}.', 'ERROR', id=self.id)
