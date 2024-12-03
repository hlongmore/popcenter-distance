from unittest import TestCase

from popcenter import coordinates
from popcenter.converters import CityStateSearch


# NOTA BENE: the coordinates in these tests may need updating every so often
#  when the database gets updated.


class TestCityStateSearch(TestCase):
    cs = CityStateSearch(simple=False)

    def test_bad_city_state(self):
        with self.assertRaises(ValueError):
            self.cs.search(None, None)
        with self.assertRaises(ValueError):
            self.cs.search('Kearns', 'UT')

    def test_salt_lake(self):
        expected = coordinates.LatLongCoordinate(40.75199, -111.8819)
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
            (40.7519, -111.8819),
            (34.070, -118.3966),
            (46.8599, -92.0540),
            (39.7699, -84.1799),
            (39.4900, -76.6500),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.cs.search_bulk(cities)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)
