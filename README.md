# Strava-Extract-Actvity-Data

Welcome to the extractions repository
This repository contains code for extracting all activities from cyclist in strava.

Steps to extract activities data:
First open "Extract athlete activities synchronous" notebook

1. create list of riders (Rider - object)
    
       rider_csv = pd.read_csv('data/some_csv.csv')
       riders = []
       for index, row in df.iterrows():
           rider = Rider(row['full_name'], row['url'], row['cyclist_id'])
           if valid_rider_url(rider.rider_url):
               riders.append(rider)
       
      
2. create an GetActivities object and provide it a username and the riders list

       get_activities = GetActivities(username, riders)

3. run the extract_activities()

       get_activities.extract_activities()
       
4. run the run()

       get_activities.run()
