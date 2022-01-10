from bs4 import BeautifulSoup
from utils import *
from browser import Browser


class LinksExtractor(Browser):

    def __init__(self, id, riders, html_files_path):
        Browser.__init__(self, id)
        self.riders = riders
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, url_param_dict):
        html_file_name = "_".join(url_param_dict.values())
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    def _fetch_rider_year_interval_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_html_file = os.listdir(rider_dir_path)[0]
            html_content = read_from_html(rider_dir_path, rider_html_file)
            rider_soup = BeautifulSoup(html_content, 'html.parser')
            options_soup = rider_soup.find('div', attrs={'class': 'drop-down-menu drop-down-sm enabled'})
            option_list = options_soup.find('ul', 'options').find_all('a')
            for time_interval in option_list:
                row = {'strava_id': rider_id,
                       'time_interval_link': f"{BASE_STRAVA_URL}{time_interval.attrs['href']}"}
                append_row_to_csv(csv_file_path, row)
        except:
            log(f'Could not fetch year interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_year_interval_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.riders:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values):
                    log(f'Fetching year interval links for cyclist {rider_id}, {i} / {len(self.riders) - 1}',
                        id=self.id)
                    self._fetch_rider_year_interval_links(rider_id, csv_file_path)
                i += 1
        except:
            log(f'Failed fetching riders year interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_week_interval_links(self, rider_id, csv_file_path):
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
                    row = {'strava_id': rider_id,
                           'time_interval_link': f"{BASE_STRAVA_URL}{week_interval.attrs['href']}"}
                    append_row_to_csv(csv_file_path, row)
                i = +1
        except:
            log(f'Could not fetch week interval links for rider {rider_id}.', 'ERROR', id=self.id)

    def extract_rider_week_interval_links(self, csv_file_path):
        try:
            rider_id = None
            i = 0
            for rider_id in self.riders:
                csv_file_exist = os.path.exists(csv_file_path)
                if (not csv_file_exist) or (
                        float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values):
                    log(f'Fetching week interval links for cyclist {rider_id}, {i} / {len(self.riders) - 1}',
                        id=self.id)
                    self._fetch_rider_week_interval_links(rider_id, csv_file_path)
                i += 1
        except:
            log(f'Failed fetching riders week interval links, current rider fetched {rider_id}', 'ERROR', id=self.id)

    def _fetch_rider_activity_links(self, rider_id, csv_file_path):
        try:
            rider_dir_path = f"{self.html_files_path}/{rider_id}"
            rider_week_interval_files = os.listdir(rider_dir_path)
            i = 0
            for week_interval_link in rider_week_interval_files:
                log(f'Fetching week interval links from file {week_interval_link}, {i} / {len(rider_week_interval_files) - 1}',
                    id=self.id, debug=False)
                html_content = read_from_html(rider_dir_path, week_interval_link)
                rider_soup = BeautifulSoup(html_content, 'html.parser')
                activities_soup = rider_soup.find('div', attrs={'class': 'feed'})
                activities_list = activities_soup.find_all('div', attrs={
                    'class': 'react-card-container'})
                for activity_card in activities_list:
                    activity_a = activity_card.find(
                        lambda tag: tag.name == "a" and "/activities/" in tag.attrs['href'])
                    if activity_a is not None:
                        activity_link = f"{BASE_STRAVA_URL}{activity_a.attrs['href']}"
                        activity_id = activity_link.split('/activities/')[1]
                        activity_not_extracted = (not os.path.exists(csv_file_path))
                        activity_not_extracted = activity_not_extracted or (
                                    float(rider_id) not in pd.read_csv(csv_file_path)['strava_id'].values)
                        activity_not_extracted = activity_not_extracted or (
                                    float(activity_id) not in pd.read_csv(csv_file_path)['activity_id'].values)
                        if activity_not_extracted:
                            print('test')
                            row = {'strava_id': rider_id,
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
            for rider_id in self.riders:
                log(f'Fetching activity links for cyclist {rider_id}, {i} / {len(self.riders) - 1}',
                    id=self.id)
                self._fetch_rider_activity_links(rider_id, csv_file_path)
                i += 1

        except:
            log(f'Failed fetching rider activity links, current rider fetched {rider_id}', 'ERROR',
                id=self.id)
