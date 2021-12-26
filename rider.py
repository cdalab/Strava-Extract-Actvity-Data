import pandas as pd
class Rider:
    def __init__(self, rider_url, rider_id, years = tuple(range(2015, 2022)), months=tuple(range(1, 13))):
        self.rider_url = rider_url
        self.rider_id = rider_id
        self.activity_links = set()
        self.links = []
        self.years = years
        self.months = months

          # tables
        self.workout = []
        self.workout_hrs = []
        self.workout_cadences = []
        self.workout_powers = []
        self.workout_speeds = []

    def to_csv(self):
        workout = pd.DataFrame(self.workout).to_csv(index = False)
        workout_hrs = pd.DataFrame(self.workout_hrs).to_csv(index = False)
        workout_cadences = pd.DataFrame(self.workout_cadences).to_csv(index = False)
        workout_powers = pd.DataFrame(self.workout_powers).to_csv(index = False)
        workout_speeds = pd.DataFrame(self.workout_speeds).to_csv(index = False)
        return workout, workout_hrs, workout_cadences, workout_powers, workout_speeds

    def to_data(self):
        return self.workout, self.workout_hrs, self.workout_cadences, self.workout_powers, self.workout_speeds
        
    def __repr__(self):
        return f'Rider_link: {self.rider_url}, Rider ID: {self.rider_id}'
