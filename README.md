# Strava-Extract-Actvity-Data

Welcome to the extractions repository.

This repository contains code for extracting all activities from cyclists in strava.

Steps to extract activities data:

### First open "Extract athlete activities synchronous" notebook

1. Create rider csv file. csv need to contain the following columns:

       full_name, url, cyclist_id

2. Create a list of riders (Rider - object)
    
       rider_csv = pd.read_csv('data/some_csv.csv')
       riders = []
       for index, row in df.iterrows():
           rider = Rider(row['full_name'], row['url'], row['cyclist_id'])
           riders.append(rider)
       
      
3. Create an GetActivities object and provide it a username and the riders list

       get_activities = GetActivities(username, riders)

4. Run the extract_activities(). It creates links fetch from the activity links

       get_activities.extract_activities()
       
5. Run the run(). It fetches activity links from the links created in step 3

       get_activities.run()
       

### Second open the "cyclists" folder with pycharm.

1. Install all the required packages

       pip install requirements.txt

2. place a pickle folder that contains list of Riders.

3. run the main.py and specify the username index, low slicing bound of riders and high slicing bound of riders. 

for example:

       menu.py 2 100 500

 will run with username[2] and riders[100:500]

