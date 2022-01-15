from urllib.parse import parse_qsl

import pandas as pd
from bs4 import BeautifulSoup
from utils import *
from browser import Browser


class LinksExtractor(Browser):

    def __init__(self, id, pages, html_files_path):
        Browser.__init__(self, id)
        self.pages = pages
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        html_file_name = "_".join(url_param_dict.values())
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    def _fetch_rider_year_interval_links(self, rider_id, csv_file_path, start_week, end_week):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_html_file = os.listdir(rider_dir_path)[0]
            html_content = read_from_html(rider_dir_path, rider_html_file)
            rider_soup = BeautifulSoup(html_content, 'html.parser')
            options_soup = rider_soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
            option_list = options_soup.find('ul', 'options').find_all('a')
            for time_interval in option_list:
                link = f"{BASE_STRAVA_URL}{time_interval.attrs['href']}"
                url_param_dict = dict(parse_qsl(link.split('?')[1]))
                interval = url_param_dict['interval']
                curr_year, curr_week = int(interval[:4]), int(interval[4:])
                start_year, s_week = int(start_week[:4]), int(start_week[4:])
                end_year, e_week = int(end_week[:4]), int(end_week[4:])
                if (start_year <= curr_year <= end_year) and (s_week <= curr_week <= e_week):
                    row = {'rider_id': rider_id,
                           'time_interval_link': link}
                    append_row_to_csv(csv_file_path, row)
        except:
            log(f'Could not fetch year interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_year_interval_links(self, csv_file_path, start_week, end_week):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['rider_id'].values):
                    log(f'Fetching year interval links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                        id=self.id)
                    self._fetch_rider_year_interval_links(rider_id, csv_file_path, start_week, end_week)
                i += 1
        except:
            log(f'Failed fetching riders year interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_week_interval_links(self, rider_id, csv_file_path, start_week, end_week):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_year_interval_files = os.listdir(rider_dir_path)
            i = 0
            for year_interval_link in rider_year_interval_files:
                log(f'Fetching week interval links from file {year_interval_link}, {i} / {len(rider_year_interval_files) - 1}',
                    id=self.id, debug=False)
                html_content = read_from_html(rider_dir_path, year_interval_link)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                rider_intervals = rider_soup.find('ul', attrs={'class': 'intervals'}).find_all('a')
                for week_interval in rider_intervals:
                    link = f"{BASE_STRAVA_URL}{week_interval.attrs['href']}"
                    url_param_dict = dict(parse_qsl(link.split('?')[1]))
                    interval = url_param_dict['interval']
                    curr_year, curr_week = int(interval[:4]), int(interval[4:])
                    start_year, s_week = int(start_week[:4]), int(start_week[4:])
                    end_year, e_week = int(end_week[:4]), int(end_week[4:])
                    if (start_year <= curr_year <= end_year) and (s_week <= curr_week <= e_week):
                        row = {'rider_id': rider_id,
                               'time_interval_link': link}
                        append_row_to_csv(csv_file_path, row)
                i += 1
        except:
            log(f'Could not fetch week interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_week_interval_links(self, csv_file_path, start_week, end_week):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['rider_id'].values):
                    log(f'Fetching week interval links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                        id=self.id)
                    self._fetch_rider_week_interval_links(rider_id, csv_file_path, start_week, end_week)
                i += 1
        except:
            log(f'Failed fetching riders week interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_activity_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_week_interval_files = os.listdir(rider_dir_path)
            i = 0
            for week_interval_link in rider_week_interval_files:
                log(f'Fetching activity links from file {week_interval_link}, {i} / {len(rider_week_interval_files) - 1}',
                    id=self.id, debug=False)
                html_content = read_from_html(rider_dir_path, week_interval_link)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                activities_soup = rider_soup.find('div', attrs={'class': 'feed'})
                activities_list = activities_soup.find_all('div', attrs={
                    'class': 'react-card-container'})
                for activity_card in activities_list:
                    a_type = activity_card.find(lambda tag: (tag.name == 'div') and ('data-react-class' in tag.attrs))
                    if a_type['data-react-class'] not in ACTIVITY_POST_TYPES:
                        log(f"New post activity type found: {a_type['data-react-class']}", 'WARNING', id=self.id)
                    activity_a = activity_card.find_all(
                        lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
                    if len(activity_a) > 0:
                        if a_type['data-react-class'] != 'GroupActivity':
                            activity_a = activity_a[0]
                        else:
                            entries = activity_card.find(lambda tag: (tag.name == 'ul') and ('class' in tag.attrs) and (
                                        'GroupActivity--list-entries' in str(tag.attrs['class'])))
                            for entry in entries.contents:
                                link = entry.find(lambda tag: tag.name == 'a' and (
                                            ('athletes' in tag.attrs['href']) or ('pros' in tag.attrs['href'])))['href']
                                if float(link.split('/')[-1]) == float(rider_id):
                                    activity_a = entry.find(
                                        lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
                                    break
                        activity_link = f"{BASE_STRAVA_URL}{activity_a.attrs['href']}"
                        activity_id = activity_link.split('/activities/')[1]
                        activity_not_extracted = (not os.path.exists(csv_file_path))
                        activity_not_extracted = activity_not_extracted or (
                                float(rider_id) not in pd.read_csv(csv_file_path)['rider_id'].values)
                        activity_not_extracted = activity_not_extracted or (
                                float(activity_id) not in pd.read_csv(csv_file_path)['activity_id'].values)
                        if activity_not_extracted:
                            row = {'rider_id': rider_id,
                                   'activity_link': activity_link,
                                   'activity_id': activity_id}
                            append_row_to_csv(csv_file_path, row)
                    else:
                        if activity_card.find('div', attrs={'data-react-class': "Activity"}) is not None:
                            raise ValueError(
                                f'Activity missed and should be recognized, interval file {week_interval_link}')
                        challenge = activity_card.find('div', attrs={'data-react-class': 'ChallengeJoin'})
                        join_club = activity_card.find('div', attrs={'data-react-class': "ClubJoin"})
                        if (challenge is None) and (join_club is None):
                            raise ValueError(
                                f'Activity card type is not recognized, interval file {week_interval_link}')
                print_progress_bar(i + 1, len(rider_week_interval_files), prefix='Progress:', suffix='Complete',
                                   length=50)
                i += 1

        except:
            log(f'Could not fetch time interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_activity_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.pages:
                log(f'Fetching activity links for cyclist {rider_id}, {i} / {len(self.pages) - 1}',
                    id=self.id)
                self._fetch_rider_activity_links(rider_id, csv_file_path)
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
                            activity_option_link in pd.read_csv(csv_file_path)['activity_option_link'].values)):
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
            log(f'Could not fetch week interval links for rider {rider_id}.', 'ERROR', id=self.id)

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
