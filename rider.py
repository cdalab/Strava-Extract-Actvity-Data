class Rider:
    def __init__(self, rider_url, strava_id, full_name, years = tuple(range(2015, 2023)), months=tuple(range(1, 13))):
        self.rider_url = rider_url
        self.strava_id = strava_id
        self.full_name=full_name
        self.activity_links = set()
        self.links = []
        self.years = years
        self.months = months

    def __repr__(self):
        return f'Rider: {self.full_name}, link: {self.rider_url}, strava id: {self.strava_id}'
