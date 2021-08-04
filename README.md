# Strava-Extract-Actvity-Data

Welcome to the Strava activity extractor repository.

This repository contains code for extracting all activities from cyclists in strava.

Steps to extract activities data:

## Install necessary packages

For pip:

    pip install requirements.txt

for conda:

    conda create --name extractor
    conda activate extractor
    conda env update --file environment.yml

## Fetch cyclists data from csv

1. Create rider csv file. The csv file needs to contain the following columns:

       full_name, url, cyclist_id,  



## CSV file format

1. Create rider csv file. The csv file needs to contain the following columns:

       full_name, url, cyclist_id, team_pcs_id
   
   > Each url needs to be in the following format:
   > -  https://www.strava.com/athletes/SOME_DIGITS 
   > 
   > -  https://www.strava.com/pros/SOME_DIGITS 
   > 
   > You can use the function `valid_rider_url` inside the `extractor/utils` to check for validation
 
   > Each team_pcs_id needs to be in the following format (it can also be empty):
   > - 1114,1542,1234,9321
  

2. Save the riders to a pickle file

       with open(f'data/riders.pickle', 'wb') as handle:
           pickle.dump(riders, handle, protocol=pk.HIGHEST_PROTOCOL)


## Get Activity Links

1. open the `extractor` folder in terminal.
2. run
   
       main.py link <riders_pickle_file> <username_index> <from_year> <to_year> <from_month> <to_month>

    > Example: 
    > 
    > `main.py link ISN_riders 2 2015 2021 1 12`
    >
    > Will run the get activity links from the ISN_riders.pickle file with username[2] from 2015 to 2021 (including) and from January to December (including)

## Get Activity Data

After fetching the activity links, we can extract data from these links.

1. open the `extractor` folder in terminal.
2. run

       mein.py data <riders_pickle_file> <username_index> <start_rider_index> <end_rider_index>

    > Exmaple:
    > 
    > `main.py data ISN_riders 2 200 500`
    > 
    >
    > - Will run the get activities data from ISN_riders.pickle file with username[2] and riders[100:500]
    > 
    > `main.py data ISN_riders 2 200 500 -i 20`
    > - will run only for all links after the index 20

## Get data with one command

1. open the `extractor` folder in terminal.
2. run
    
       main.py flow <riders_csv_file> <username_index>

    > Example:
    > 
    > `main.py flow rider_csv 2`
    >
    > will run all commands (create pickle, link, data) and save data to csv file
    >
    > `main.py flow rider_csv 2 -i 100 153 164`
    >
    > will run only for riders that belong to the teams 100, 153 and 164 


