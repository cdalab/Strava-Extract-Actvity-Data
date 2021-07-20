class Rider:
    def __init__(self, rider_name, rider_url, rider_id):
        self.rider_name = rider_name.lower()
        self.rider_url = rider_url
        self.rider_id = rider_id
        self.activity_links = set()
        self.links = []
        
        # tables
        self.workout = []
        self.workout_hrs = []
        self.workout_cadences = []
        self.workout_powers = []
        self.workout_speeds = []
        
    def __repr__(self):
        return f'Rider_link: {self.rider_url}, Rider name: {self.rider_name}, Rider ID: {self.rider_id}'
