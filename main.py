import json
import os
from pathlib import Path
import pandas as pd
from LinksDownloader import LinksDownloader
from DataExtractor import DataExtractor
from utils import log, setting_up, check_int, append_row_to_csv
from consts import *


def download_rider_pages(urls_file_path, id, html_files_path='link/riders_time_interval_pages', low_limit_index=0,
                         high_limit_index=None, overwrite_mode=None, riders=None, users=USERS):
    log("---- START DOWNLOADING RIDER PAGES ----", id=id)
    riders_df = pd.read_csv(f"{urls_file_path}")
    riders_df = riders_df[riders_df['strava_link'].notna()]
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [float(e.replace('\n', '')) for e in f.readlines()]
        riders_df = riders_df[riders_df['strava_id'].isin(riders_in_files)]
    else:
        if high_limit_index is not None:
            riders_df = riders_df.iloc[low_limit_index:high_limit_index - 1]
        else:
            riders_df = riders_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_df, html_files_path=html_files_path,
                                 id=id, users=users)
    downloader.download_rider_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING RIDER PAGES ----", id=id)


def extract_rider_year_interval_links(id, html_files_path=None,
                                      csv_file_path=None, global_csv_file_path='link/riders_year_interval_links.csv',
                                      riders=None,
                                      low_limit_index=0, high_limit_index=None, week_range=None, start_year=None):
    log("---- START EXTRACTING YEAR INTERVAL LINKS ----", id=id)
    riders_list = os.listdir(html_files_path)
    start_week, end_week = None, None
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    if high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    if week_range is not None:
        week_range = json.loads(week_range)
        start_week, end_week = str(week_range[0]), str(week_range[1])
    links_extractor = DataExtractor(pages=riders_list, id=id, html_files_path=html_files_path)
    links_extractor.extract_rider_year_interval_links(csv_file_path, global_csv_file_path, start_year, start_week,
                                                      end_week)

    log("---- FINISHED EXTRACTING YEAR INTERVAL LINKS ----", id=id)


def download_time_interval_pages(id, csv_file_path
                                 , html_files_path=None, low_limit_index=0, global_csv_file_path=None,
                                 high_limit_index=None, overwrite_mode=None, riders=None, users=USERS, start_year=None):
    log("---- START DOWNLOADING TIME INTERVAL PAGES ----", id=id)

    riders_intervals_links_df = pd.DataFrame()
    if os.path.exists(csv_file_path):
        riders_intervals_links_df = pd.read_csv(csv_file_path)
    if os.path.exists(global_csv_file_path):
        riders_intervals_links_df = pd.concat([riders_intervals_links_df, pd.read_csv(global_csv_file_path)])
    riders_intervals_links_df = riders_intervals_links_df.loc[~riders_intervals_links_df['time_interval_link'].isna()]
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [float(e.replace('\n', '')) for e in f.readlines()]
        riders_intervals_links_df = riders_intervals_links_df[
            riders_intervals_links_df['rider_id'].isin(riders_in_files)]
    else:
        if high_limit_index is not None:
            riders_intervals_links_df = riders_intervals_links_df.iloc[low_limit_index:high_limit_index]
        else:
            riders_intervals_links_df = riders_intervals_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_intervals_links_df, id=id, users=users, html_files_path=html_files_path)
    downloader.download_time_interval_pages(start_year, overwrite_mode)

    log("---- FINISHED DOWNLOADING TIME INTERVAL PAGES ----", id=id)


def extract_rider_week_interval_links(id, html_files_path=None,
                                      csv_file_path=None, global_csv_file_path='link/riders_week_interval_links.csv',
                                      low_limit_index=0, high_limit_index=None, riders=None, week_range=None,
                                      start_year=None):
    log("---- START EXTRACTING WEEK INTERVAL LINKS ----", id=id)
    riders_list = os.listdir(html_files_path)
    start_week, end_week = None, None
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    elif high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    if week_range is not None:
        week_range = json.loads(week_range)
        start_week, end_week = str(week_range[0]), str(week_range[1])
    links_extractor = DataExtractor(pages=riders_list, id=id, html_files_path=html_files_path)
    links_extractor.extract_rider_week_interval_links(csv_file_path, global_csv_file_path, start_year, start_week,
                                                      end_week)

    log("---- FINISHED EXTRACTING WEEK INTERVAL LINKS ----", id=id)


def extract_rider_activity_links(id, html_files_path=None,
                                 csv_file_path=None, global_csv_file_path='link/riders_activity_links.csv',
                                 low_limit_index=0,
                                 high_limit_index=None, riders=None, start_year=None):
    log("---- START EXTRACTING ACTIVITY LINKS ----", id=id)
    riders_list = os.listdir(html_files_path)
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    elif high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    links_extractor = DataExtractor(pages=riders_list,
                                    id=id,
                                    html_files_path=html_files_path)
    links_extractor.extract_rider_activity_links(csv_file_path, global_csv_file_path, start_year)

    log("---- FINISHED EXTRACTING ACTIVITY LINKS ----", id=id)


def download_activity_pages(id, csv_file_path=None, html_files_path='link/riders_activity_pages',
                            global_csv_file_path='link/riders_activity_links.csv', low_limit_index=0,
                            high_limit_index=None, riders=None, overwrite_mode=None, users=USERS):
    log("---- START DOWNLOADING ACTIVITY PAGES ----", id=id)

    riders_activity_links_df = pd.DataFrame()
    if os.path.exists(csv_file_path):
        riders_activity_links_df = pd.read_csv(csv_file_path)
    if os.path.exists(global_csv_file_path):
        riders_activity_links_df = pd.concat([riders_activity_links_df, pd.read_csv(global_csv_file_path)])
    riders_activity_links_df = riders_activity_links_df.loc[~riders_activity_links_df['activity_link'].isna()]
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [float(e.replace('\n', '')) for e in f.readlines()]
        riders_activity_links_df = riders_activity_links_df.loc[
            riders_activity_links_df['rider_id'].isin(riders_in_files)]
    elif high_limit_index is not None:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:high_limit_index]
    else:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_activity_links_df, id=id, users=users, html_files_path=html_files_path)
    downloader.download_activity_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING ACTIVITY PAGES ----", id=id)


def extract_activity_analysis_links(id, html_files_path='link/riders_activity_pages',
                                    csv_file_path='link/activity_analysis_links.csv', low_limit_index=0,
                                    high_limit_index=None, riders=None):
    log("---- START EXTRACTING ACTIVITY ANALYSIS LINKS ----", id=id)
    riders_list = os.listdir(html_files_path)
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    elif high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    links_extractor = DataExtractor(pages=riders_list,
                                    id=id,
                                    html_files_path=html_files_path)
    links_extractor.extract_activity_analysis_links(csv_file_path)

    log("---- FINISHED EXTRACTING ACTIVITY ANALYSIS LINKS ----", id=id)


def download_activity_analysis_pages(id, csv_file_path='link/activity_analysis_links.csv',
                                     html_files_path='link/riders_activity_pages', low_limit_index=0,
                                     high_limit_index=None, riders=None, overwrite_mode=None, users=USERS):
    log("---- START DOWNLOADING ANALYSIS ACTIVITY PAGES ----", id=id)

    riders_activity_links_df = pd.read_csv(f"{csv_file_path}")
    riders_activity_links_df = riders_activity_links_df.loc[~riders_activity_links_df['activity_option_link'].isna()]
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [float(e.replace('\n', '')) for e in f.readlines()]
        riders_activity_links_df = riders_activity_links_df.loc[
            riders_activity_links_df['rider_id'].isin(riders_in_files)]
    elif high_limit_index is not None:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:high_limit_index]
    else:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_activity_links_df, id=id, users=users, html_files_path=html_files_path)
    downloader.download_activity_analysis_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING ANALYSIS ACTIVITY PAGES ----", id=id)


def extract_data_from_analysis_activities(id, html_files_path='link/riders_activity_pages',
                                          low_limit_index=0, high_limit_index=None, riders=None, data_types=None):
    log("---- START EXTRACTING ACTIVITY ANALYSIS DATA ----", id=id)
    riders_list = os.listdir(html_files_path)
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    elif high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    links_extractor = DataExtractor(pages=riders_list,
                                    id=id,
                                    html_files_path=html_files_path)
    links_extractor.extract_data_from_analysis_activities(data_types=data_types)

    log("---- FINISHED EXTRACTING ACTIVITY ANALYSIS DATA ----", id=id)


def restore_activities_from_backup(id, html_files_path='link/riders_activity_pages',
                                   low_limit_index=0, high_limit_index=None, riders=None, data_types=None):
    log("---- START RESTORING ACTIVITY ANALYSIS PAGES ----", id=id)
    riders_list = os.listdir(html_files_path)
    if riders is not None:
        with open(riders) as f:
            riders_in_files = [e.replace('\n', '') for e in f.readlines()]
        riders_list = [r for r in riders_list if r in riders_in_files]
    elif high_limit_index is not None:
        riders_list = riders_list[low_limit_index:high_limit_index]
    else:
        riders_list = riders_list[low_limit_index:]
    links_extractor = DataExtractor(pages=riders_list,
                                    id=id,
                                    html_files_path=html_files_path)
    links_extractor.restore_activities_from_backup(data_types=data_types)
    log("---- FINISHED RESTORING ACTIVITY ANALYSIS PAGES ----", id=id)


if __name__ == '__main__':
    # users input example: -u {\"start\":0,\"step\":18}

    args = setting_up()
    command = args['command']
    id = args['id']
    users = args['users']
    start_year = args['start_year']
    if users is None:
        users = USERS

    if command == 'download_rider_pages':
        # run example : main.py -c download_rider_pages -if data/all_cyclists_strava_urls.csv-t 2
        # run example : main.py -c download_rider_pages -if data/ISN_merged_strava_urls.csv -li 10 -hi 100 -o 1
        riders = args['riders']
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        urls_file_path = args['input_file']
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        overwrite_mode = args['overwrite_mode']

        if urls_file_path is None:
            urls_file_path = 'data/all_cyclists_strava_urls.csv'
        urls_file_path = f"{urls_file_path.replace('.csv', '')}.csv"
        # Changed to be constant
        html_files_path = args['output_file']
        if html_files_path is None:
            html_files_path = "link/riders_time_interval_pages"
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING RIDER INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_rider_pages(urls_file_path, id, html_files_path, low_limit_index=low_limit_index,
                                     high_limit_index=high_limit_index, overwrite_mode=overwrite_mode, riders=riders,
                                     users=users)
            else:
                download_rider_pages(urls_file_path, id, html_files_path, overwrite_mode=overwrite_mode, riders=riders,
                                     users=users)

        except:
            log(f'Problem in download_rider_pages function, '
                f'args: {urls_file_path, html_files_path, low_limit_index, high_limit_index, riders, overwrite_mode}',
                'ERROR', id=id)

    elif command == 'extract_rider_year_interval_links':
        # run example : main.py -c extract_rider_year_interval_links  -of link/riders_year_interval_links.csv
        # run example : main.py -c extract_rider_year_interval_links -li 10 -hi 100
        riders = args['riders']
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']

        # Changed to be constant
        html_files_path = args['input_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"

        csv_file_path = args['output_file']
        week_range = args['week_range']
        if csv_file_path is None:
            csv_file_path = f'link/{id}/riders_year_interval_links'
        csv_file_path = f"{csv_file_path.replace('.csv', '')}.csv"
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_year_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  low_limit_index=low_limit_index, riders=riders,
                                                  high_limit_index=high_limit_index, start_year=start_year)
            else:
                extract_rider_year_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  week_range=week_range, riders=riders, start_year=start_year)

        except:
            log(f'Problem in extract_rider_year_interval_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, week_range, riders, start_year}',
                'ERROR', id=id)

    elif command == 'download_year_interval_pages':
        # run example : main.py -c download_year_interval_pages -if link/riders_year_interval_links.csv
        # run example : main.py -c download_year_interval_pages -li 10 -hi 100

        riders = args['riders']
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']

        if csv_file_path is None:
            csv_file_path = f"link/{id}/riders_year_interval_links"
        csv_file_path = f"{csv_file_path.replace('.csv', '')}.csv"

        # Changed to be constant
        html_files_path = args['output_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING TIME INTERVAL INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_time_interval_pages(id, csv_file_path, html_files_path,
                                             low_limit_index=low_limit_index,
                                             global_csv_file_path='link/riders_year_interval_links.csv',
                                             high_limit_index=high_limit_index, overwrite_mode=overwrite_mode,
                                             users=users, riders=riders, start_year=start_year)
            else:
                download_time_interval_pages(id, csv_file_path, html_files_path,
                                             global_csv_file_path='link/riders_year_interval_links.csv',
                                             overwrite_mode=overwrite_mode,
                                             users=users, riders=riders, start_year=start_year)

        except:
            log(f'Problem in download_year_interval_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, overwrite_mode, riders, start_year}',
                'ERROR', id=id)

    elif command == 'extract_rider_week_interval_links':
        # run example : main.py -c extract_rider_week_interval_links -of link/riders_week_interval_links -r "data\riders tracking\111-10.txt"
        # run example : main.py -c extract_rider_week_interval_links -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']

        # Changed to be constant
        html_files_path = args['input_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"

        csv_file_path = args['output_file']
        riders = args['riders']
        week_range = args['week_range']
        if csv_file_path is None:
            csv_file_path = f'link/{id}/riders_week_interval_links'
        # if (low_limit_index is not None) or (high_limit_index is not None):
        #     csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        # if high_limit_index is not None:
        #     csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_week_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  low_limit_index=low_limit_index, high_limit_index=high_limit_index,
                                                  riders=riders, start_year=start_year)
            else:
                extract_rider_week_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  riders=riders, week_range=week_range, start_year=start_year)

        except:
            log(f'Problem in extract_rider_week_interval_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, week_range, start_year}',
                'ERROR', id=id)

    elif command == 'download_week_interval_pages':
        # run example : main.py -c download_week_interval_pages -if link/riders_week_interval_links.csv -t 2
        # run example : main.py -c download_week_interval_pages -li 10 -hi 100

        riders = args['riders']
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']

        # Changed to be constant
        html_files_path = args['output_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"
        Path(html_files_path).mkdir(parents=True, exist_ok=True)

        if csv_file_path is None:
            csv_file_path = f'link/{id}/riders_week_interval_links.csv'
        csv_file_path = f"{csv_file_path.replace('.csv', '')}.csv"
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING TIME INTERVAL INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_time_interval_pages(id, csv_file_path, html_files_path,
                                             low_limit_index=low_limit_index,
                                             global_csv_file_path='link/riders_week_interval_links.csv',
                                             high_limit_index=high_limit_index, overwrite_mode=overwrite_mode,
                                             users=users, riders=riders, start_year=start_year)
            else:
                download_time_interval_pages(id, csv_file_path, html_files_path,
                                             global_csv_file_path='link/riders_week_interval_links.csv',
                                             overwrite_mode=overwrite_mode,
                                             users=users, riders=riders, start_year=start_year)

        except:
            log(f'Problem in download_year_interval_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, overwrite_mode, riders, start_year}',
                'ERROR', id=id)

    elif command == 'extract_rider_activity_links':
        # run example : main.py -c extract_rider_activity_links -of link/riders_activity_links.csv -r "data\riders tracking\111-10.txt"
        # run example : main.py -c extract_rider_activity_links -li 10 -hi 100
        # insert -li or -hi is the index of rider (not index of link)
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']

        # Changed to be constant
        html_files_path = args['input_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"

        csv_file_path = args['output_file']
        riders = args['riders']
        if csv_file_path is None:
            csv_file_path = f'link/{id}/riders_activity_links'
        # if (low_limit_index is not None) or (high_limit_index is not None):
        #     csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        # if high_limit_index is not None:
        #     csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path.replace(".csv", "")}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_activity_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                             low_limit_index=low_limit_index, high_limit_index=high_limit_index,
                                             riders=riders, start_year=start_year)
            else:
                extract_rider_activity_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                             riders=riders, start_year=start_year)

        except:
            log(f'Problem in extract_rider_activity_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, riders, start_year}',
                'ERROR', id=id)

    elif command == 'download_activity_pages':
        # run example : main.py -c download_activity_pages -if link/riders_activity_links.csv -of link/riders_activity_pages  -r "data\riders tracking\111-10.txt"
        # run example : main.py -c download_activity_pages -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']
        riders = args['riders']
        if csv_file_path is None:
            csv_file_path = f'link/{id}/riders_activity_links'
        csv_file_path = f"{csv_file_path.replace('.csv', '')}.csv"

        if html_files_path is None:
            html_files_path = f"link/riders_activity_pages"
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING ACTIVITIES INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_activity_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                        high_limit_index=high_limit_index, overwrite_mode=overwrite_mode, users=users,
                                        riders=riders)
            else:
                download_activity_pages(id, csv_file_path, html_files_path, riders=riders,
                                        overwrite_mode=overwrite_mode, users=users)

        except:
            log(f'Problem in download_activity_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'extract_activity_analysis_links':
        # run example : main.py -c extract_activity_analysis_links -if link/riders_activity_pages -of link/additional_activity_analysis_links.csv
        # insert -li or -hi is the index of rider (not index of link)
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        riders = args['riders']

        if csv_file_path is None:
            csv_file_path = f'link/{id}/activity_analysis_links'
        csv_file_path = f'{csv_file_path.replace(".csv", "")}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_activity_analysis_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                low_limit_index=low_limit_index, high_limit_index=high_limit_index,
                                                riders=riders)
            else:
                extract_activity_analysis_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                riders=riders)

        except:
            log(f'Problem in extract_activity_analysis_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'download_activity_analysis_pages':
        # run example : main.py -c download_activity_analysis_pages -if link/activity_analysis_links.csv -of link/riders_activity_pages -r "data\riders tracking\111-10.txt"
        # run example : main.py -c download_activity_analysis_pages -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        riders = args['riders']
        overwrite_mode = args['overwrite_mode']
        data_types = args['data_types']

        if html_files_path is None:
            html_files_path = f"link/riders_activity_pages"

        if csv_file_path is None:
            csv_file_path = f'link/{id}/activity_analysis_links'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING ACTIVITIES INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_activity_analysis_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                                 high_limit_index=high_limit_index, overwrite_mode=overwrite_mode,
                                                 users=users, riders=riders)
            else:
                download_activity_analysis_pages(id, csv_file_path, html_files_path, riders=riders,
                                                 overwrite_mode=overwrite_mode, users=users)

        except:
            log(f'Problem in download_activity_analysis_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'extract_data_from_analysis_activities':
        # run example : main.py -c extract_data_from_analysis_activities -if link/riders_activity_pages -r "data\riders tracking\111-10.txt" -dt [\"overview\"]
        # insert -li or -hi is the index of rider (not index of link)
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        riders = args['riders']
        data_types = args['data_types']

        if html_files_path is None:
            html_files_path = f"link/riders_activity_pages"

        if csv_file_path is None:
            csv_file_path = f'link/{id}/activity_link_types'
        csv_file_path = f'{csv_file_path.replace(".csv", "")}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_data_from_analysis_activities(id, html_files_path=html_files_path,
                                                      low_limit_index=low_limit_index,
                                                      high_limit_index=high_limit_index, riders=riders,
                                                      data_types=data_types)
            else:
                extract_data_from_analysis_activities(id, html_files_path=html_files_path,
                                                      riders=riders, data_types=data_types)

        except:
            log(f'Problem in extract_data_from_analysis_activities function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, riders, data_types}',
                'ERROR', id=id)


    elif command == 'restore_activities_from_backup':
        # run example : main.py -c restore_activities_from_backup -if link/riders_activity_pages -dt [\"overview\"]

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        riders = args['riders']
        data_types = args['data_types']
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                restore_activities_from_backup(id, html_files_path=html_files_path,
                                               low_limit_index=low_limit_index,
                                               high_limit_index=high_limit_index, data_types=data_types)
            else:
                restore_activities_from_backup(id, html_files_path=html_files_path,
                                               riders=riders, data_types=data_types)

        except:
            log(f'Problem in restore_activities_from_backup function, '
                f'args: {html_files_path, low_limit_index, high_limit_index, riders, data_types}',
                'ERROR', id=id)

    elif command == 'change_time_interval_file_names':
        # run example : main.py -c change_time_interval_file_names

        # Changed to be constant
        html_files_path = args['input_file']
        if html_files_path is None:
            html_files_path = f"link/riders_time_interval_pages"
        try:
            riders_pages = os.listdir(html_files_path)
            i = 1
            for rider in riders_pages:
                print(f"Rider\t{rider}\t{i}/{len(riders_pages)}")
                rider_dir_path = f"{html_files_path}/{rider}"
                if os.path.isdir(rider_dir_path):
                    for html in os.listdir(rider_dir_path):
                        time_interval_path = f"{rider_dir_path}/{html}"
                        time_interval_path_parts = time_interval_path.replace('.html', '').split('_')
                        last_part = time_interval_path_parts[-1]
                        if not check_int(last_part):
                            continue
                        time_interval_path_new = f"{'_'.join(time_interval_path_parts[:-1])}.html"
                        if os.path.exists(time_interval_path_new):
                            os.remove(time_interval_path)
                        else:
                            os.rename(time_interval_path, time_interval_path_new)
                i += 1

        except:
            log(f'Problem in change_time_interval_file_names function',
                'ERROR', id=id)

    elif command == 'unify_all_computers_csv_files':
        # run example : main.py -c unify_all_computers_csv_files -if M:/Maor/STRAVA -of M:/Maor/STRAVA/Strava-Extract-Actvity-Data
        # TODO: test after changes of new locations
        input_path = args['input_file']
        output_path = args['output_file']
        if input_path is None:
            input_path = "M:/Maor/STRAVA/link"
        if output_path is None:
            output_path = "M:/Maor/STRAVA/Strava-Extract-Actvity-Data"
        try:
            computers = list(filter(lambda f: output_path != f'{input_path}/{f}', os.listdir(input_path)))
            computers = [c for c in computers if os.path.isdir(c)]
            i = 1
            for c in computers:
                log(f"Computer\t{c}\t{i}/{len(computers)}")
                c_dir_path = f"{input_path}/{c}"
                for file in os.listdir(f"{c_dir_path}/link"):
                    if ('.csv' in file) and (file not in CSV_FILES_TO_IGNORE):
                        csv_content = pd.read_csv(f"{c_dir_path}/link/{file}")
                        file_exists = os.path.exists(f'{output_path}/link/{file}')
                        if file_exists:
                            csv_content.to_csv(f'{output_path}/link/{file}', mode='a', index=False, header=False)
                        else:
                            csv_content.to_csv(f'{output_path}/link/{file}', index=False, header=True)

                i += 1
            for file in os.listdir(f'{output_path}/link'):
                if ('.csv' in file) and (file not in CSV_FILES_TO_IGNORE):
                    unified_df = pd.read_csv(f'{output_path}/link/{file}')
                    unified_unique_records_df = unified_df.drop_duplicates()
                    unified_unique_records_df.to_csv(f'{output_path}/link/{file}', index=False, header=True)
        except:
            log(f'Problem in unify_all_computers_csv_files function',
                'ERROR', id=id)

    else:
        raise ValueError('Invalid command')

    # TODO: download the other pages of activities
    # TODO: pay attention to the different structure of indoor cycling activities and virtual rides
    # TODO:: after run extract links of activity analysis check errors - for the case of wrong metrics!
    # TODO: validate all unit are as expected
    # TODO: validate the activity map to the right rider! can be wrong because of groups activities
    # TODO: after extract all activity links again - check in log info if more types of activities exist
    # TODO: add to download activity overview = check if the title in head contains "Ride", elswise - valueError (it could help to recognize activities such as Races that are not Ride)
    # TODO: download all activity pages again (overwrite off, done for download the races!)

    # TODO: create one flow for riders?

    log("---- FINISH ----", id=id)
