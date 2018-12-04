from unittest import TestCase

import coordinates
from converters.zip import ZipSearch


class TestZipSearch(TestCase):
    zs = ZipSearch(simple=False)

    def test_relatively_new_zip_code(self):
        # NOTA BENE: this test may need updating every so often when the
        # database gets updated.
        expected = coordinates.LatLongCoordinate(41.5, 52.1)
        actual = self.zs.search('84129')
        self.assertAlmostEqual(expected.latitude, actual.latitude)
        self.assertAlmostEqual(expected.longitude, actual.longitude)

    def test_established_zip_code(self):
        expected = coordinates.LatLongCoordinate(41.5, 52.1)
        actual = self.zs.search('84101')
        self.assertAlmostEqual(expected.latitude, actual.latitude)
        self.assertAlmostEqual(expected.longitude, actual.longitude)

    def test_bulk_search(self):
        codes = [84129, 84118, 90210, 45302, 21030]
        points = [
            (1.1, 1.2), (2.1, 2.2), (43.1, 123.3), (45.23, 54.2), (123.4, 34.0),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.zs.search_bulk(codes)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude)
