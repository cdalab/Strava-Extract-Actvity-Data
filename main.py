import os
from pathlib import Path
import pandas as pd
from links_downloader import LinksDownloader
from link_extractor import LinksExtractor
from utils import log, setting_up


def download_rider_pages(urls_file_path, id, html_files_path='link/riders_time_interval_pages', low_limit_index=0,
                         high_limit_index=None,overwrite_mode=None):
    log("---- START DOWNLOADING RIDER PAGES ----", id=id)

    riders_df = pd.read_csv(f"{urls_file_path}")
    riders_df = riders_df[riders_df['strava_link'].notna()]
    if high_limit_index is not None:
        riders_df = riders_df.iloc[low_limit_index:high_limit_index - 1]
    else:
        riders_df = riders_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_df, html_files_path=html_files_path,
                                 id=id)
    downloader.download_rider_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING RIDER PAGES ----", id=id)


def extract_rider_year_interval_links(id, html_files_path='link/riders_time_interval_pages',
                                      csv_file_path='link/riders_year_interval_links.csv',
                                      low_limit_index=0, high_limit_index=None,start_week=None,end_week=None):
    log("---- START EXTRACTING YEAR INTERVAL LINKS ----", id=id)
    riders = os.listdir(html_files_path)
    if high_limit_index is not None:
        riders = riders[low_limit_index:high_limit_index]
    else:
        riders = riders[low_limit_index:]
    links_extractor = LinksExtractor(pages=riders, id=id, html_files_path=html_files_path)
    links_extractor.extract_rider_year_interval_links(csv_file_path,start_week,end_week)

    log("---- FINISHED EXTRACTING YEAR INTERVAL LINKS ----", id=id)


def download_time_interval_pages(id, csv_file_path,
                                 html_files_path='link/riders_time_interval_pages', low_limit_index=0,
                                 high_limit_index=None,overwrite_mode=None):
    log("---- START DOWNLOADING TIME INTERVAL PAGES ----", id=id)

    riders_intervals_links_df = pd.read_csv(f"{csv_file_path}")
    riders_intervals_links_df = riders_intervals_links_df.loc[~riders_intervals_links_df['time_interval_link'].isna()]
    if high_limit_index is not None:
        riders_intervals_links_df = riders_intervals_links_df.iloc[low_limit_index:high_limit_index]
    else:
        riders_intervals_links_df = riders_intervals_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_intervals_links_df, id=id, html_files_path=html_files_path)
    downloader.download_time_interval_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING TIME INTERVAL PAGES ----", id=id)


def extract_rider_week_interval_links(id, html_files_path='link/riders_time_interval_pages',
                                      csv_file_path='link/riders_week_interval_links.csv',
                                      low_limit_index=0, high_limit_index=None, riders_input=None, start_week=None, end_week=None):
    log("---- START EXTRACTING WEEK INTERVAL LINKS ----", id=id)
    riders = os.listdir(html_files_path)
    if riders_input is not None:
        riders = [str(r) for r in riders if (float(r) in riders_input)]
    elif high_limit_index is not None:
        riders = riders[low_limit_index:high_limit_index]
    else:
        riders = riders[low_limit_index:]
    links_extractor = LinksExtractor(pages=riders, id=id, html_files_path=html_files_path)
    links_extractor.extract_rider_week_interval_links(csv_file_path, start_week, end_week)

    log("---- FINISHED EXTRACTING WEEK INTERVAL LINKS ----", id=id)


def extract_rider_activity_links(id, html_files_path='link/riders_time_interval_pages',
                                 csv_file_path='link/riders_activity_links.csv', low_limit_index=0,
                                 high_limit_index=None, riders_input=None):
    log("---- START EXTRACTING ACTIVITY LINKS ----", id=id)
    riders = os.listdir(html_files_path)
    if riders_input is not None:
        riders = [str(r) for r in riders if (float(r) in riders_input)]
    elif high_limit_index is not None:
        riders = riders[low_limit_index:high_limit_index]
    else:
        riders = riders[low_limit_index:]
    links_extractor = LinksExtractor(pages=riders,
                                     id=id,
                                     html_files_path=html_files_path)
    links_extractor.extract_rider_activity_links(csv_file_path)

    log("---- FINISHED EXTRACTING ACTIVITY LINKS ----", id=id)


def download_activity_pages(id, csv_file_path='link/riders_activity_links.csv',
                            html_files_path='link/riders_activity_pages', low_limit_index=0,
                            high_limit_index=None, riders_input=None,overwrite_mode=None):
    log("---- START DOWNLOADING ACTIVITY PAGES ----", id=id)

    riders_activity_links_df = pd.read_csv(f"{csv_file_path}")
    riders_activity_links_df = riders_activity_links_df.loc[~riders_activity_links_df['activity_link'].isna()]
    if riders_input is not None:
        riders_activity_links_df = riders_activity_links_df.loc[riders_activity_links_df['rider_id'].isin(riders)]
    elif high_limit_index is not None:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:high_limit_index]
    else:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_activity_links_df, id=id, html_files_path=html_files_path)
    downloader.download_activity_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING ACTIVITY PAGES ----", id=id)


def extract_activity_analysis_links(id, html_files_path='link/riders_activity_pages',
                                    csv_file_path='link/activity_analysis_links.csv', low_limit_index=0,
                                    high_limit_index=None, riders_input=None):
    log("---- START EXTRACTING ACTIVITY ANALYSIS LINKS ----", id=id)
    riders = os.listdir(html_files_path)
    if riders_input is not None:
        riders = [str(r) for r in riders if (float(r) in riders_input)]
    elif high_limit_index is not None:
        riders = riders[low_limit_index:high_limit_index]
    else:
        riders = riders[low_limit_index:]
    links_extractor = LinksExtractor(pages=riders,
                                     id=id,
                                     html_files_path=html_files_path)
    links_extractor.extract_activity_analysis_links(csv_file_path)

    log("---- FINISHED EXTRACTING ACTIVITY ANALYSIS LINKS ----", id=id)


def download_activity_analysis_pages(id, csv_file_path='link/activity_analysis_links.csv',
                            html_files_path='link/riders_activity_pages', low_limit_index=0,
                            high_limit_index=None, riders_input=None,overwrite_mode=None):
    log("---- START DOWNLOADING ANALYSIS ACTIVITY PAGES ----", id=id)

    riders_activity_links_df = pd.read_csv(f"{csv_file_path}")
    riders_activity_links_df = riders_activity_links_df.loc[~riders_activity_links_df['activity_option_link'].isna()]
    if riders_input is not None:
        riders_activity_links_df = riders_activity_links_df.loc[riders_activity_links_df['rider_id'].isin(riders)]
    elif high_limit_index is not None:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:high_limit_index]
    else:
        riders_activity_links_df = riders_activity_links_df.iloc[low_limit_index:]
    downloader = LinksDownloader(riders=riders_activity_links_df, id=id, html_files_path=html_files_path)
    downloader.download_activity_analysis_pages(overwrite_mode)

    log("---- FINISHED DOWNLOADING ANALYSIS ACTIVITY PAGES ----", id=id)


if __name__ == '__main__':

    args = setting_up()
    command = args['command']
    id = args['id']

    if command == 'download_rider_pages':
        # run example : main.py -c download_rider_pages -if data/ISN_merged_strava_urls.csv -of link/riders_time_interval_pages -t 2
        # run example : main.py -c download_rider_pages -if data/ISN_merged_strava_urls.csv -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        urls_file_path = args['input_file']
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        overwrite_mode=args['overwrite_mode']
        if html_files_path is None:
            html_files_path = 'link/riders_time_interval_pages'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING RIDER INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_rider_pages(urls_file_path, id, html_files_path, low_limit_index=low_limit_index,
                                     high_limit_index=high_limit_index,overwrite_mode=overwrite_mode)
            else:
                download_rider_pages(urls_file_path, id, html_files_path,overwrite_mode=overwrite_mode)

        except:
            log(f'Problem in download_rider_pages function, '
                f'args: {urls_file_path, html_files_path, low_limit_index, high_limit_index,overwrite_mode}',
                'ERROR', id=id)

    elif command == 'extract_rider_year_interval_links':
        # run example : main.py -c extract_rider_year_interval_links -if link/riders_time_interval_pages -of link/riders_year_interval_links -t 2
        # run example : main.py -c extract_rider_year_interval_links -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        start_week = args['start_week']
        end_week = args['end_week']
        if csv_file_path is None:
            csv_file_path = f'link/riders_year_interval_links'
        csv_file_path = f'{csv_file_path}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_year_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_rider_year_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,start_week=start_week,end_week=end_week)

        except:
            log(f'Problem in extract_rider_year_interval_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index,start_week,end_week}',
                'ERROR', id=id)

    elif command == 'download_year_interval_pages':
        # run example : main.py -c download_year_interval_pages -if link/riders_year_interval_links.csv -of link/riders_time_interval_pages -t 2
        # run example : main.py -c download_year_interval_pages -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']
        if csv_file_path is None:
            csv_file_path = 'link/riders_time_interval_pages'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING TIME INTERVAL INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_time_interval_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                             high_limit_index=high_limit_index,overwrite_mode=overwrite_mode)
            else:
                download_time_interval_pages(id, csv_file_path, html_files_path,overwrite_mode=overwrite_mode)

        except:
            log(f'Problem in download_year_interval_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, overwrite_mode}',
                'ERROR', id=id)

    elif command == 'extract_rider_week_interval_links':
        # run example : main.py -c extract_rider_week_interval_links -if link/riders_time_interval_pages -of link/riders_week_interval_links -r [6913455.0]
        # run example : main.py -c extract_rider_week_interval_links -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        riders = args['riders']
        start_week = args['start_week']
        end_week = args['end_week']
        if csv_file_path is None:
            csv_file_path = f'link/riders_week_interval_links'
        # if (low_limit_index is not None) or (high_limit_index is not None):
        #     csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        # if high_limit_index is not None:
        #     csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_week_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_rider_week_interval_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                  riders_input=riders,start_week=start_week,end_week=end_week)

        except:
            log(f'Problem in extract_rider_week_interval_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, start_week, end_week}',
                'ERROR', id=id)

    elif command == 'download_week_interval_pages':
        # run example : main.py -c download_week_interval_pages -if link/riders_week_interval_links.csv -of link/riders_time_interval_pages -t 2
        # run example : main.py -c download_week_interval_pages -li 10 -hi 100
        # "C:\Users\User\OneDrive - post.bgu.ac.il\STRAVA data\link\riders_time_interval_pages"

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']
        if csv_file_path is None:
            csv_file_path = 'link/riders_time_interval_pages'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING TIME INTERVAL INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_time_interval_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                             high_limit_index=high_limit_index,overwrite_mode=overwrite_mode)
            else:
                download_time_interval_pages(id, csv_file_path, html_files_path,overwrite_mode=overwrite_mode)

        except:
            log(f'Problem in download_year_interval_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, overwrite_mode}',
                'ERROR', id=id)

    elif command == 'extract_rider_activity_links':
        # run example : main.py -c extract_rider_activity_links -if link/riders_time_interval_pages -of link/riders_activity_links.csv -r [6913455.0]
        # run example : main.py -c extract_rider_activity_links -li 10 -hi 100
        # insert -li or -hi is the index of rider (not index of link)
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        riders = args['riders']
        if csv_file_path is None:
            csv_file_path = f'link/riders_activity_links'
        # if (low_limit_index is not None) or (high_limit_index is not None):
        #     csv_file_path = f'{csv_file_path}_from_{low_limit_index}'
        # if high_limit_index is not None:
        #     csv_file_path = f'{csv_file_path}_till_{high_limit_index}'
        csv_file_path = f'{csv_file_path.replace(".csv", "")}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_rider_activity_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                             low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_rider_activity_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                             riders_input=riders)

        except:
            log(f'Problem in extract_rider_activity_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'download_activity_pages':
        # run example : main.py -c download_activity_pages -if link/riders_activity_links.csv -of link/riders_activity_pages  -r [6913455.0]
        # run example : main.py -c download_activity_pages -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        overwrite_mode = args['overwrite_mode']
        riders = args['riders']
        if csv_file_path is None:
            csv_file_path = 'link/riders_activity_links'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING ACTIVITIES INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_activity_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                        high_limit_index=high_limit_index,overwrite_mode=overwrite_mode)
            else:
                download_activity_pages(id, csv_file_path, html_files_path, riders_input=riders,overwrite_mode=overwrite_mode)

        except:
            log(f'Problem in download_activity_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'extract_activity_analysis_links':
        # run example : main.py -c extract_activity_analysis_links -if link/riders_activity_pages -of link/activity_analysis_links.csv
        # insert -li or -hi is the index of rider (not index of link)
        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['input_file']
        csv_file_path = args['output_file']
        riders = args['riders']
        if csv_file_path is None:
            csv_file_path = f'link/activity_analysis_links'
        csv_file_path = f'{csv_file_path.replace(".csv", "")}.csv'
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING LINK INDEX: {low_limit_index}_{high_limit_index}', id=id)
                extract_activity_analysis_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                low_limit_index=low_limit_index, high_limit_index=high_limit_index)
            else:
                extract_activity_analysis_links(id, html_files_path=html_files_path, csv_file_path=csv_file_path,
                                                riders_input=riders)

        except:
            log(f'Problem in extract_activity_analysis_links function, '
                f'args: {html_files_path, csv_file_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)

    elif command == 'download_activity_analysis_pages':
        # run example : main.py -c download_activity_analysis_pages -if link/activity_analysis_links.csv -of link/riders_activity_pages  -r [6913455.0]
        # run example : main.py -c download_activity_analysis_pages -li 10 -hi 100

        num_of_threads = args['num_of_threads'] if args['num_of_threads'] else 1
        low_limit_index = args['low_limit_index']
        high_limit_index = args['high_limit_index']
        html_files_path = args['output_file']
        csv_file_path = args['input_file']
        riders = args['riders']
        overwrite_mode = args['overwrite_mode']
        if csv_file_path is None:
            csv_file_path = 'link/activity_analysis_links'
        Path(html_files_path).mkdir(parents=True, exist_ok=True)
        try:
            if (low_limit_index is not None) or (high_limit_index is not None):
                log(f'STARTING ACTIVITIES INDEX: {low_limit_index}_{high_limit_index}', id=id)
                download_activity_analysis_pages(id, csv_file_path, html_files_path, low_limit_index=low_limit_index,
                                                 high_limit_index=high_limit_index,overwrite_mode=overwrite_mode)
            else:
                download_activity_analysis_pages(id, csv_file_path, html_files_path, riders_input=riders,overwrite_mode=overwrite_mode)

        except:
            log(f'Problem in download_activity_analysis_pages function, '
                f'args: {csv_file_path, html_files_path, low_limit_index, high_limit_index, riders}',
                'ERROR', id=id)




    # TODO: download the other pages of activities
    # TODO: pay attention to the different structure of indoor cycling activities and virtual rides
    # TODO:: after run extract links of activity analysis check errors - for the case of wrong metrics!
    # TODO: validate all unit are as expected
    # TODO: validate the activity map to the right rider! can be wrong because of groups activities
    # TODO: after extract all activity links again - check in log info if more types of activities exist
    #TODO: add to download activity overview = check if the title in head contains "Ride", elswise - valueError (it could help to recognize activities such as Races that are not Ride)
    # TODO: download all activity pages again (overwrite off, done for download the races!)

    # TODO: create one flow for riders?


    log("---- FINISH ----", id=id)
