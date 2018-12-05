from collections import Counter

from uszipcode import SearchEngine

from popcenter.coordinates import LatLongCoordinate
from .city_state import CityStateSearch

class ZipSearch:

    def __init__(self, simple=True):
        self.engine = SearchEngine(simple_zipcode=simple)

    def search(self, zipcode):
        data = self.engine.by_zipcode(zipcode)
        if data.lat and data.lng:
            return LatLongCoordinate(data.lat, data.lng)
        else:
            return CityStateSearch(engine=self.engine).search(
                data.major_city, data.state)

    def search_bulk(self, zipcodes):
        latlong_coordinates = []
        for zc in zipcodes:
            latlong_coordinates.append(self.search(zc))
        return latlong_coordinates

    def get_county(self, coordinates: LatLongCoordinate):
        zipcodes = self.engine.by_coordinates(coordinates.latitude, coordinates.longitude)
        c = Counter([z.county for z in zipcodes])
        return c.most_common()[0][0]
