import firebase_admin
import pandas as pd
from rider import Rider
from firebase_admin import credentials, storage

def init_firebase():
    cred = credentials.Certificate("strava-extractor-firebase-adminsdk-he2li-c87e8d06cf.json")
    firebase_admin.initialize_app(cred, {'storageBucket': 'strava-extractor.appspot.com'})

def upload_data_firebase(name, data):

    bucket = storage.bucket()
    blob = bucket.blob(f'{name}')
    blob.upload_from_string(data)




