from bs4 import BeautifulSoup
from utils import *
from browser import Browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.parse import parse_qsl


def save_activity_type(rider_activity, activity_type):
    if not rider_activity["activity_link"] in pd.read_csv('link/activity_link_types.csv').values:
        row = {'rider_id': rider_activity["rider_id"],
               'activity_link': rider_activity["activity_link"],
               'activity_id': rider_activity["activity_id"],
               'activity_type': activity_type}
        append_row_to_csv('link/activity_link_types.csv', row)


class LinksDownloader(Browser):

    def __init__(self, id, riders, html_files_path):
        Browser.__init__(self, id)
        self.riders = riders
        self.html_files_path = html_files_path

    def _get_interval_html_file_and_dir(self, strava_id, link):
        url_param_dict = dict(parse_qsl(link.split('?')[1]))
        year_offset = url_param_dict['year_offset']
        interval = url_param_dict['interval']
        interval_type = url_param_dict['interval_type']
        chart_type = url_param_dict['chart_type']
        html_file_name = f"{interval}_{interval_type}_{chart_type}_{year_offset}"
        html_file_dir = f"{self.html_files_path}/{strava_id}"
        return html_file_dir, html_file_name

    @download_files_wrapper
    def _rider_page_general_handler(self, html_file_name):
        return {html_file_name: self.browser.page_source}

    @timeout_wrapper
    def _download_rider_page(self, i, rider, overwrite_mode=None):
        info_msg = f'Fetching page for cyclist {rider["full_name"]}, {i} / {len(self.riders) - 1}'
        self.browser.get(rider['strava_link'])
        response = self._is_valid_html(rider['strava_link'])
        if response is not None:
            return response
        # t.sleep(random.random() + random.randint(0, 1))
        intervals_graph = WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located((By.ID, "interval-graph")))
        WebDriverWait(intervals_graph, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "options")))
        week_btn = WebDriverWait(intervals_graph, 2).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Weekly")))
        first_link = week_btn.get_attribute('href')
        html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider['strava_id'],
                                                                             first_link)
        wrapper_args = (info_msg, html_file_dir, [html_file_name], overwrite_mode)
        self._rider_page_general_handler(*wrapper_args, html_file_name)

    @driver_wrapper
    def download_rider_pages(self, overwrite_mode=None):
        try:
            rider = None
            i = 0
            for idx, rider in self.riders.iterrows():
                # t.sleep(random.random())
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider['rider_id'],
                                                                                     rider['time_interval_link'])
                if get_overwrite_pred(html_file_dir, html_file_name, overwrite_mode):
                    link_fetch_error_msg = f'Could not fetch rider {rider["full_name"]}, id {rider["strava_id"]}.'
                    self._download_rider_page(link_fetch_error_msg, i,
                                              **dict(rider=rider, overwrite_mode=overwrite_mode))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {rider}', 'ERROR', id=self.id)

    @timeout_wrapper
    def _download_rider_time_interval_page(self, prev_interval_range, i,
                                           rider_time_interval, overwrite_mode=None):
        self.browser.get(rider_time_interval['time_interval_link'])
        response = self._is_valid_html(rider_time_interval['time_interval_link'])
        if response is not None:
            return response
        # t.sleep(random.random() + 0.5 + random.randint(2, 4))
        current_interval_range_element = WebDriverWait(self.browser, 3).until(
            EC.presence_of_element_located((By.ID, "interval-value")))
        current_interval_range = current_interval_range_element.text
        if prev_interval_range == current_interval_range:
            raise ValueError(f'The relevant interval page has not loaded yet')
        feed = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "feed")))
        num_of_activities = len(feed.find_elements(By.XPATH, "./*"))
        if num_of_activities > 0:
            WebDriverWait(self.browser, 5).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "react-card-container")))
            html_file_dir, html_file_name = self._get_interval_html_file_and_dir(rider_time_interval['rider_id'],
                                                                                 rider_time_interval[
                                                                                     'time_interval_link'])
            info_msg = f'Fetching page for cyclist {rider_time_interval["rider_id"]}, file {html_file_name}, {i} / {len(self.riders) - 1}'
            wrapper_args = (info_msg, html_file_dir, [html_file_name], overwrite_mode)
            self._rider_page_general_handler(*wrapper_args, html_file_name)
            return current_interval_range

    @driver_wrapper
    def download_time_interval_pages(self, overwrite_mode=None):
        try:
            time_interval = None
            prev_year_interval_range = None
            i = 0
            for idx, time_interval in self.riders.iterrows():
                # t.sleep(random.random())
                html_file_dir, html_file_name = self._get_interval_html_file_and_dir(time_interval['rider_id'],
                                                                                     time_interval[
                                                                                         'time_interval_link'])
                if get_overwrite_pred(html_file_dir, html_file_name, overwrite_mode):
                    link_fetch_error_msg = f'Could not fetch time interval {time_interval["time_interval_link"]}, for rider {time_interval["rider_id"]}.'
                    prev_year_interval_range = self._download_rider_time_interval_page(link_fetch_error_msg,
                                                                                       prev_year_interval_range, i,
                                                                                       **dict(
                                                                                           rider_time_interval=time_interval,
                                                                                           overwrite_mode=overwrite_mode))
                i += 1
        except:
            log(f'Failed fetching riders pages, current rider fetched {time_interval}', 'ERROR', id=self.id)

    @timeout_wrapper
    def _download_rider_activity_pages(self, prev_activity, i, rider_activity, overwrite_mode=None):
        activity_url = f'{rider_activity["activity_link"].replace("/overview", "")}/overview'
        self.browser.get(activity_url)
        # t.sleep(random.random() + 0.5 + random.randint(1, 3))
        response = self._is_valid_html(activity_url)
        if response is not None:
            return response
        heading = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "heading")))
        details = WebDriverWait(heading, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "details")))
        current_activity_title = details.text
        activity_details = WebDriverWait(heading, 2).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "ul")))
        current_activity = ''.join([ad.text for ad in activity_details]) + current_activity_title
        if prev_activity == current_activity:
            raise ValueError(f'The relevant activity page has not loaded yet')
        title = WebDriverWait(heading, 7).until(EC.visibility_of_element_located((By.TAG_NAME, "h2"))).text
        deli_idx = title.find('–')
        activity_type = title[deli_idx + 1:].strip() if deli_idx > 0 else None
        save_activity_type(rider_activity, activity_type)
        if activity_type in ACTIVITY_TYPES_TO_IGNORE:
            return current_activity
        WebDriverWait(heading, 7).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "li")))
        if activity_type == 'Indoor Cycling':
            self.browser.find_element(By.PARTIAL_LINK_TEXT, 'Overview').click()
            view = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "view")))
            stacked_chart = WebDriverWait(view, 3).until(EC.visibility_of_element_located((By.ID, "stacked-chart")))
            self._wait_for_chart(stacked_chart)
            WebDriverWait(stacked_chart, 3).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "label-box")))

        html_file_dir = f"{self.html_files_path}/{rider_activity['rider_id']}/{rider_activity['activity_id']}"
        info_msg = f'Fetching activity page for cyclist {rider_activity["rider_id"]}, activity {rider_activity["activity_id"]}, {i} / {len(self.riders) - 1}'
        wrapper_args = (info_msg, html_file_dir, ["overview"], overwrite_mode)
        self._rider_page_general_handler(*wrapper_args, "overview")
        return current_activity

    @driver_wrapper
    def download_activity_pages(self, overwrite_mode=None):
        try:
            activity = None
            prev_activity = None
            i = 0
            for idx, activity in self.riders.iterrows():
                html_file_dir = f"{self.html_files_path}/{activity['rider_id']}/{activity['activity_id']}"

                if get_overwrite_pred(html_file_dir, "overview", overwrite_mode):
                    # t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch activity {activity["activity_id"]}, for rider {activity["rider_id"]}.'
                    prev_activity = self._download_rider_activity_pages(link_fetch_error_msg,
                                                                        prev_activity, i,
                                                                        **dict(
                                                                            rider_activity=activity,
                                                                            overwrite_mode=overwrite_mode))
                i += 1
        except:
            log(f'Failed fetching riders activity pages, current activity fetched {activity}.', 'ERROR', id=self.id)

    @download_files_wrapper
    def _handle_analysis_page_case(self, rider_activity, data_container):
        elev_chart = WebDriverWait(data_container, 3).until(
            EC.visibility_of_element_located((By.ID, "elevation-chart")))
        self._wait_for_chart(elev_chart)
        stacked_chart = WebDriverWait(data_container, 3).until(
            EC.visibility_of_element_located((By.ID, "stacked-chart")))
        self._wait_for_chart(stacked_chart)
        WebDriverWait(stacked_chart, 3).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "label-box")))
        distance_metric_activity = self.browser.page_source
        axis_icons = WebDriverWait(stacked_chart, 3).until(
            EC.visibility_of_all_elements_located((By.TAG_NAME, "image")))
        for icon in axis_icons:
            if 'time' in icon.get_attribute('href'):
                icon.click()
                break
        elev_chart = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((By.ID, "elevation-chart")))
        self._wait_for_chart(elev_chart)
        stacked_chart = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((By.ID, "stacked-chart")))
        self._wait_for_chart(stacked_chart)
        time_metric_activity = self.browser.page_source
        if distance_metric_activity == time_metric_activity:
            raise ValueError(f'The time metric analysis has not loaded yet, activity: {rider_activity["activity_id"]}')
        return {f"{rider_activity['option_type'][1:]}_distance": distance_metric_activity,
                f"{rider_activity['option_type'][1:]}_time": time_metric_activity}

    def _wait_for_chart(self, chart):
        WebDriverWait(chart, 5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "svg")))
        WebDriverWait(chart, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'defs')))
        WebDriverWait(chart, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'rect')))
        WebDriverWait(chart, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'g')))
        WebDriverWait(chart, 3).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'line')))
        WebDriverWait(chart, 3).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'path')))

    @download_files_wrapper
    def _handle_power_charts_page(self, rider_activity, data_container):
        chart = WebDriverWait(data_container, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "power-charts")))
        self._wait_for_chart(chart)
        watts_metric_activity = self.browser.page_source
        WebDriverWait(data_container, 2).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'KG'))).click()
        chart = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "power-charts")))
        self._wait_for_chart(chart)
        watts_kg_metric_activity = self.browser.page_source
        if watts_metric_activity == watts_kg_metric_activity:
            raise ValueError(
                f'The watts/kg curve has not loaded yet, activity: {rider_activity["activity_id"]}')
        if 'This athlete has not set their weight.' in watts_kg_metric_activity:
            return {f"{rider_activity['option_type'][1:]}_watts": watts_metric_activity}
        return {f"{rider_activity['option_type'][1:]}_watts": watts_metric_activity,
                f"{rider_activity['option_type'][1:]}_watts-kg": watts_kg_metric_activity}

    @download_files_wrapper
    def _handle_power_distribution_page(self, rider_activity, data_container):
        chart = WebDriverWait(data_container, 3).until(
            EC.visibility_of_element_located((By.ID, "power-dist-chart")))
        self._wait_for_chart(chart)
        return {f"{rider_activity['option_type'][1:]}": self.browser.page_source}

    @download_files_wrapper
    def _handle_table_page(self, rider_activity, data_container):
        table = WebDriverWait(data_container, 3).until(
            EC.visibility_of_element_located((By.TAG_NAME, "table")))
        WebDriverWait(table, 3).until(EC.visibility_of_element_located((By.TAG_NAME, "tr")))
        WebDriverWait(table, 3).until(EC.visibility_of_element_located((By.TAG_NAME, "td")))
        return {f"{rider_activity['option_type'][1:]}": self.browser.page_source}

    @timeout_wrapper
    def download_analysis_pages_loop(self, prev_activity, i, rider_activity, overwrite_mode=None):
        info_msg = f'Fetching {rider_activity["option_type"]} activity page for cyclist {rider_activity["rider_id"]}, activity {rider_activity["activity_id"]}, {i} / {len(self.riders) - 1}'
        html_file_dir = f"{self.html_files_path}/{rider_activity['rider_id']}/{rider_activity['activity_id']}"
        files = ACTIVITY_ANALYSIS_FILES[rider_activity["option_type"]]
        wrapper_args = (info_msg, html_file_dir, files, overwrite_mode)
        href = rider_activity["activity_option_link"].split(BASE_STRAVA_URL)[-1]
        side_menu = WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((By.ID, 'pagenav')))
        WebDriverWait(side_menu, 2).until(EC.element_to_be_clickable((By.XPATH, f'*//a[@href="{href}"]'))).click()
        view = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.ID, "view")))
        data_container = WebDriverWait(view, 2).until(EC.visibility_of_element_located((By.XPATH, 'section')))
        current_activity = self.browser.page_source
        if prev_activity == current_activity:
            raise ValueError(f'The relevant activity page has not loaded yet')
        section_id = data_container.get_attribute('id')
        # /analysis
        if section_id == 'basic-analysis':
            self._handle_analysis_page_case(*wrapper_args, rider_activity, data_container)
            return current_activity
        header = WebDriverWait(data_container, 2).until(EC.visibility_of_element_located((By.XPATH, 'header')))
        WebDriverWait(header, 2).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'li')))
        chart_container = WebDriverWait(data_container, 2).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(@class, 'inset main')]")))
        chart_header = chart_container.find_element(By.TAG_NAME, 'h2').text
        # /power-curve, /est-power-curve
        if chart_header.find('Power Curve') > -1:
            self._handle_power_charts_page(*wrapper_args, rider_activity, chart_container)
            return current_activity

        # /power-distribution , /est-power-distribution
        if chart_header.find('Power Distribution') > -1:
            self._handle_power_distribution_page(*wrapper_args, rider_activity, chart_container)
            return current_activity

        # /zone-distribution ,/heartrate
        if (chart_header.find('Zone Distribution') > -1) or (chart_header.find('Heart Rate') > -1):
            self._handle_table_page(*wrapper_args, rider_activity, chart_container)
            return current_activity

        # unfamiliar chart header
        log(f'Unfamiliar activity header {chart_header}, activity {rider_activity["activity_id"]}', 'WARNING',
            id=self.id)
        wrapper_args = (info_msg, html_file_dir, [f"{rider_activity['option_type'][1:]}_unknown"], overwrite_mode)
        self._rider_page_general_handler(*wrapper_args, f"{rider_activity['option_type'][1:]}_unknown")
        return current_activity

    @timeout_wrapper
    def _download_rider_activity_analysis_pages(self, prev_activity, i, rider_activity, overwrite_mode=None):
        self.browser.get(rider_activity["activity_option_link"])
        # t.sleep(random.random() + 0.5 + random.randint(1, 3))
        response = self._is_valid_html(rider_activity["activity_option_link"])
        if response is not None:
            return response
        error_msg = f'Could not fetch {rider_activity["option_type"]} activity of cyclist {rider_activity["rider_id"]}, activity {rider_activity["activity_id"]}.'
        return self.download_analysis_pages_loop(error_msg, prev_activity, i, **dict(rider_activity=rider_activity,
                                                                                     overwrite_mode=overwrite_mode))

    def _download_indoor_ride_again(self, rider_id, activity_id):
        html_dir_path = f"{self.html_files_path}/{rider_id}/{activity_id}"
        html_content = read_from_html(html_dir_path, 'overview.html')
        activity_soup = BeautifulSoup(html_content, 'html.parser')
        stacked_chart = activity_soup.find('div', attrs={'id': 'stacked-chart'})
        if stacked_chart is None:
            return True
        base_chart = stacked_chart.find('div', attrs={'class': 'base-chart'})
        if (base_chart is None) or (len(base_chart.contents) == 0):
            return True
        paths = stacked_chart.find_all('path', attrs={'class': 'simple-line'})
        lines = stacked_chart.find_all(lambda tag: (tag.name == 'g') and ('clip-path' in tag.attrs))
        if len(paths) != len(lines):
            return True
        boxes = stacked_chart.find_all('g', attrs={'class': 'label-box'})
        if len(boxes) != len(paths):
            return True
        return False

    def _handle_indoor_cycling_overview_page(self, rider_id, activity_id):
        download_overview_again = self._download_indoor_ride_again(rider_id, activity_id)
        if download_overview_again:
            csv_path = 'link/overview_links_to_download_again.csv'
            csv_exists = os.path.exists(csv_path)
            activity_link = f"{BASE_STRAVA_URL}/activities/{activity_id}"
            if (not csv_exists) or (activity_link not in pd.read_csv(csv_path)['activity_link'].values):
                activity_of_overview = {'rider_id': rider_id,
                                        'activity_link': activity_link,
                                        'activity_id': activity_id}
                append_row_to_csv(csv_path, activity_of_overview)

    @driver_wrapper
    def download_activity_analysis_pages(self, overwrite_mode=None):
        try:
            activity = None
            prev_activity = None
            indoor_activities_handled = set()
            i = 0
            for idx, activity in self.riders.iterrows():
                activity_id = activity['activity_id']
                rider_id = activity['rider_id']
                is_indoor = (activity['activity_type'] == 'Indoor Cycling')
                if is_indoor and (activity_id not in indoor_activities_handled):
                    self._handle_indoor_cycling_overview_page(rider_id, activity_id)
                    indoor_activities_handled.add(activity_id)
                files = ACTIVITY_ANALYSIS_FILES[activity["option_type"]]
                dir = f"{self.html_files_path}/{rider_id}/{activity_id}"
                if get_overwrite_pred(dir, files, overwrite_mode):
                    # t.sleep(random.random())
                    link_fetch_error_msg = f'Could not fetch activity {activity_id}, for rider {activity["rider_id"]}.'
                    prev_activity = self._download_rider_activity_analysis_pages(link_fetch_error_msg,
                                                                                 prev_activity, i,
                                                                                 **dict(
                                                                                     rider_activity=activity,
                                                                                     overwrite_mode=overwrite_mode))
                i += 1
        except:
            log(f'Failed fetching rider analisys activity pages, current activity fetched {activity}.', 'ERROR',
                id=self.id)
