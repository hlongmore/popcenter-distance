from collections import Counter

from uszipcode import SearchEngine

from coordinates import LatLongCoordinate


class CityStateSearch:

    def __init__(self, simple=True, engine=None):
        self.engine = engine or SearchEngine(simple_zipcode=simple)

    def search(self, city, state):
        if not city or not state:
            raise ValueError(f'Bad city/state: {city}, {state}')
        zipcodes = self.engine.by_city_and_state(city, state)
        # Get average lat/long using only zip codes that have them set.
        zc = [z for z in zipcodes if z.lat and z.lng]
        print(f'{city}, {state}')
        n = len(zc)
        if n < 1:
            raise ValueError(f'No lat/long for {city}, {state}')
        lat = sum(z.lat for z in zc)/n
        lng = sum(z.lng for z in zc)/n
        return LatLongCoordinate(lat, lng)

    def search_bulk(self, city_state_pairs):
        latlong_coordinates = []
        for city, state in city_state_pairs:
            latlong_coordinates.append(self.search(city, state))
        return latlong_coordinates

    def get_county(self, coordinates: LatLongCoordinate):
        zipcodes = self.engine.by_coordinates(coordinates.latitude, coordinates.longitude)
        c = Counter([z.county for z in zipcodes])
        return c.most_common()[0][0]
