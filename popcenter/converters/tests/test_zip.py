from unittest import TestCase

from popcenter import coordinates
from popcenter.converters.zip import ZipSearch


# NOTA BENE: the coordinates in these tests may need updating every so often
#  when the database gets updated.


class TestZipSearch(TestCase):
    zs = ZipSearch(simple=False)

    def test_relatively_new_zip_code(self):
        expected = coordinates.LatLongCoordinate(40.6599, -111.930)
        actual = self.zs.search('84129')
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_established_zip_code(self):
        expected = coordinates.LatLongCoordinate(40.7500, -111.900)
        actual = self.zs.search('84101')
        self.assertAlmostEqual(expected.latitude, actual.latitude, places=3)
        self.assertAlmostEqual(expected.longitude, actual.longitude, places=3)

    def test_bulk_search(self):
        codes = [84129, 84118, 90210, 45302, 21030]
        points = [
            (40.6599, -111.9300),
            (40.650, -112.010),
            (34.090, -118.4099),
            (40.390, -84.1700),
            (39.4699, -76.6299),
        ]
        expected = [coordinates.LatLongCoordinate(a, b) for a, b in points]
        actual = self.zs.search_bulk(codes)
        self.assertEqual(len(expected), len(actual))
        for i in range(len(expected)):
            with self.subTest(i=i):
                self.assertAlmostEqual(expected[i].latitude, actual[i].latitude, places=3)
                self.assertAlmostEqual(expected[i].longitude, actual[i].longitude, places=3)
