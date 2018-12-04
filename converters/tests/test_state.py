import os
from unittest import TestCase

import coordinates
from converters.state import StateSearch, CensusDataDownloader


class TestCensusDataDownloader(TestCase):

    def setUp(self):
        self.d = CensusDataDownloader()

    def test_download_no_file_present(self):
        self.d = CensusDataDownloader()
        self.d.download()
        self.assertTrue(d.saved_file)
        self.assertTrue(os.path.isfile(d.saved_file))

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
        expected = coordinates.LatLongCoordinate(41.5, 52.1)
        actual = self.ss.search(state)
        self.assertAlmostEqual(expected.latitude, actual.latitude)
        self.assertAlmostEqual(expected.longitude, actual.longitude)

    def test_full_state_name(self):
        state = 'New York'
        expected = coordinates.LatLongCoordinate(41.5, 52.1)
        actual = self.ss.search(state)
        self.assertAlmostEqual(expected.latitude, actual.latitude)
        self.assertAlmostEqual(expected.longitude, actual.longitude)

    def test_bulk_search(self):
        states = ['North Dakota', 'Washington', 'Maryland', 'Florida', 'Iowa']
        points = [
            (1.1, 1.2), (2.1, 2.2), (43.1, 123.3), (45.23, 54.2), (123.4, 34.0),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.ss.search_bulk(states)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude)

    def test_incorrect_state_close_enough(self):
        states = ['New Yuck', 'North Lakota', 'Utep', 'Tejas', 'Wsahingtion']
        points = [
            (1.1, 1.2), (2.1, 2.2), (43.1, 123.3), (45.23, 54.2), (123.4, 34.0),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.ss.search_bulk(states)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude)

    def test_incorrect_state_cannot_resolve(self):
        states = ['Paris', 'Dominican Republic', 'NZ', 'Norcal', 'SOCAL']
        points = [
            (1.1, 1.2), (2.1, 2.2), (43.1, 123.3), (45.23, 54.2), (123.4, 34.0),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.ss.search_bulk(states)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude)
