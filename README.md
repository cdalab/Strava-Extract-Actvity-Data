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

## Prepare cyclists list from CSV

1. Create rider csv file. The csv file needs to contain the following columns:

       full_name, url, cyclist_id

2. Create a list of riders (Rider - object)
    
       rider_csv = pd.read_csv('data/some_csv.csv')
       riders = []
       for index, row in df.iterrows():
           rider = Rider(row['full_name'], row['url'], row['cyclist_id'])
           riders.append(rider)
        
    Each url needs to be in the following format:

      https://www.strava.com/athletes/SOME_DIGITS 
      https://www.strava.com/pros/SOME_DIGITS 
   
    You can use the function `valid_rider_url` inside the `extractor/utils` to check for validation
       
3. Save the riders to a pickle file

       with open(f'data/riders.pickle', 'wb') as handle:
           pk.dump(riders, handle, protocol=pk.HIGHEST_PROTOCOL)

    

## Get Activity Links

Before fetching the activity data, we need to fetch all the activity links of the riders

1. open the `extractor` folder in terminal.
2. run
   
       main.py link <riders_pickle_file> <username_index> <from_year> <to_year> <from_month> <to_month>

    example: `main.py link ISN_riders 2 2015 2021 1 12`
   
    Will run the get activity links from the ISN_riders.pickle file with username[2] from 2015 to 2021 (including) and from January to December (including)

## Get Activity Data

After fetching the activity links, we can extract data from these links.

1. open the `extractor` folder in terminal.
3. run

       menu.py data <riders_pickle_file> <username_index> <start_rider_index> <end_rider_index>

    exmaple: `main.py data ISN_riders 2 200 500`
   
    Will run the get activities data from ISN_riders.pickle file with username[2] and riders[100:500]

