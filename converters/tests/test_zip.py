from unittest import TestCase

import coordinates
from converters.zip import ZipSearch


class TestZipSearch(TestCase):
    zs = ZipSearch(simple=False)

    def test_relatively_new_zip_code(self):
        # NOTA BENE: this test may need updating every so often when the
        # database gets updated.
        expected = coordinates.LatLongCoordinate(40.762, -111.892)
        actual = self.zs.search('84129')
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_established_zip_code(self):
        expected = coordinates.LatLongCoordinate(40.7599, -111.900)
        actual = self.zs.search('84101')
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_bulk_search(self):
        codes = [84129, 84118, 90210, 45302, 21030]
        points = [
            (40.762, -111.892),
            (40.650, -112.040),
            (34.100, -118.420),
            (40.400, -84.200),
            (39.490, -76.660),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.zs.search_bulk(codes)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)
