import os
from unittest import TestCase

from popcenter import coordinates
from popcenter.converters.state import StateSearch, CensusDataDownloader


class TestCensusDataDownloader(TestCase):

    def setUp(self):
        self.d = CensusDataDownloader()

    def test_download_no_file_present(self):
        self.d = CensusDataDownloader()
        self.d.download()
        self.assertTrue(self.d.saved_file)
        self.assertTrue(os.path.isfile(self.d.saved_file))

    def test_download_file_present(self):
        pass

    def test_download_update_available(self):
        pass

    def test_download_look_earlier(self):
        self.d.year_setup(earlier=True)
        self.d.url_setup()
        self.d.download()


class TestStateSearch(TestCase):
    ss = StateSearch()

    def test_search_two_letter_state(self):
        state = 'UT'
        expected = coordinates.LatLongCoordinate(40.401, -111.927)
        actual = self.ss.search(state)
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_full_state_name(self):
        state = 'New York'
        expected = coordinates.LatLongCoordinate(41.501, -74.621)
        actual = self.ss.search(state)
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_bulk_search(self):
        states = ['North Dakota', 'Washington', 'Maryland', 'Florida', 'Iowa']
        points = [
            (47.348, -99.310),
            (47.331, -121.620),
            (39.141, -76.798),
            (27.823, -81.635),
            (41.946, -93.037),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.ss.search_bulk(states)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)

    def test_incorrect_state_close_enough(self):
        states = ['New Yuck', 'North Lakota', 'Tejas', 'Wsahingtion']
        points = [
            (43.155, -71.462), (47.348, -99.310), (30.905, -97.366), (47.331, -121.620),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.ss.search_bulk(states)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)

    def test_incorrect_state_cannot_resolve(self):
        states = ['Paris', 'Dominican Republic', 'NZ', 'Norcal', 'SOCAL']
        for s in states:
            with self.subTest(i=s):
                with self.assertRaises(ValueError):
                    self.ss.search(s)
