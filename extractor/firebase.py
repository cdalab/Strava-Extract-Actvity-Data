import firebase_admin
import pandas as pd
from rider import Rider
from firebase_admin import credentials, storage

def upload_riders(name, riders):
    cred = credentials.Certificate("strava-extractor-firebase-adminsdk-he2li-c87e8d06cf.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'strava-extractor.appspot.com'})
    table_names = ['workout', 'workout_hrs', 'workout_cadences', 'workout_powers', 'workout_speeds']
    bucket = storage.bucket()

    workout, workout_hrs, workout_cadences, workout_powers, workout_speeds = [], [], [], [], []
    for rider in riders:
        r_workout, r_workout_hrs, r_workout_cadences, r_workout_powers, r_workout_speeds = rider.to_data()
        workout += r_workout
        workout_hrs += r_workout_hrs
        workout_cadences += r_workout_cadences
        workout_powers += r_workout_powers
        workout_speeds += r_workout_speeds

    workout = pd.DataFrame(workout).to_csv()
    workout_hrs = pd.DataFrame(workout_hrs).to_csv()
    workout_cadences = pd.DataFrame(workout_cadences).to_csv()
    workout_powers = pd.DataFrame(workout_powers).to_csv()
    workout_speeds = pd.DataFrame(workout_speeds).to_csv()

    tables = [workout, workout_hrs, workout_cadences, workout_powers, workout_speeds]


    for i in range(len(table_names)):
        blob = bucket.blob(f'{name}_{table_names[i]}.csv')

        blob.upload_from_string(str(tables[i]))




