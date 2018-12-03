from unittest import TestCase


import geodistance


class TestGeoDistance(TestCase):

    def setUp(self):
        self.rhode_island = (41.753609, -071.450869)
        self.new_york = (41.501299, -074.620909)

    def test_new_york_to_rhode_island_metric(self):
        ri = geodistance.LatLongCoordinate(*self.rhode_island)
        ny = geodistance.LatLongCoordinate(*self.new_york)
        gd = geodistance.GeoDistance(ri, ny)
        distance = gd.keerthana()
        self.assertAlmostEqual(distance, 264.842, places=3)

    def test_new_york_to_rhode_island_imperial(self):
        ri = geodistance.LatLongCoordinate(*self.rhode_island)
        ny = geodistance.LatLongCoordinate(*self.new_york)
        gd = geodistance.GeoDistance(ri, ny)
        distance = gd.keerthana(units='imperial')
        self.assertAlmostEqual(distance, 164.565, places=3)
