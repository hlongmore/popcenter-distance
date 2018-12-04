from itertools import combinations

from uszipcode import SearchEngine

from coordinates import LatLongCoordinate


class ZipSearch:

    def __init__(self, simple=True):
        self.engine = SearchEngine(simple_zipcode=simple)

    def search(self, zipcode):
        data = self.engine.by_zipcode(zipcode)
        if not data.lat or not data.lng:
            # ZipCode is missing data. Try to figure it out from the major_city.
            near_zips = self.engine.by_city_and_state(data.major_city, data.state)
            n = len(near_zips)
            data.lat = sum(z.lat for z in near_zips)/n
            data.lng = sum(z.lng for z in near_zips)/n
        return LatLongCoordinate(data.lat, data.lng)

    def search_bulk(self, zipcodes):
        latlong_coordinates = []
        for zc in zipcodes:
            latlong_coordinates.append(self.search(zc))
        return latlong_coordinates
