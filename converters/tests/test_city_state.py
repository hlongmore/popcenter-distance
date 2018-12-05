from unittest import TestCase

import coordinates
from converters.city_state import CityStateSearch


class TestCityStateSearch(TestCase):
    cs = CityStateSearch(simple=False)

    def test_bad_city_state(self):
        with self.assertRaises(ValueError):
            self.cs.search(None, None)
        with self.assertRaises(ValueError):
            self.cs.search('Kearns', 'UT')

    def test_salt_lake(self):
        expected = coordinates.LatLongCoordinate(40.762, -111.892)
        actual = self.cs.search('Salt Lake City', 'UT')
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_bulk_search(self):
        cities = [
            ('Salt Lake City', 'UT'),
            ('Beverly Hills', 'CA'),
            ('Duluth', 'MN'),
            ('Dayton', 'OH'),
            ('Hunt Valley', 'MD'),
        ]
        points = [
            (40.762, -111.892),
            (34.075, -118.400),
            (46.864, -92.058),
            (39.777, -84.185),
            (39.488, -76.657),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.cs.search_bulk(cities)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)
