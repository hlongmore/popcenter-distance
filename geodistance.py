"""
Functions for computing the geographical distance between two pairs of
latitude, longitude points.
"""
import math
from decimal import Decimal


class LatLongCoordinate:
    radians_conversion_factor = Decimal(math.pi / 180)

    def __init__(self, lat, long):
        self.latitude = Decimal(lat)
        self.longitude = Decimal(long)

    def convert_to_radians(self):
        """
        Convert the current coordinates from lat/long to rad.
        """
        return (self.latitude * self.radians_conversion_factor,
                self.longitude * self.radians_conversion_factor)


class GeoDistance:
    miles_per_km = 0.621371

    def __init__(self, *args):
        self.coord_1 = None
        self.coord_2 = None
        for i, attr_name in enumerate(['coord_1', 'coord_2']):
            if hasattr(args[i], 'latitude') and hasattr(args[i], 'longitude'):
                setattr(self, attr_name, args[i])
            elif hasattr(args[i], '__getitem__') and len(args[i] > 1):
                setattr(self, attr_name, LatLongCoordinate(args[i][0], args[i][1]))
            else:
                raise ValueError(f'Invalid type for {self.__class__.__name__}: {args}')

    @staticmethod
    def keerthana_compute_radius(latitude):
        equatorial_radius = 6378.137
        er_squared = math.pow(equatorial_radius, 2)
        polar_radius = 6356.752
        pr_squared = math.pow(polar_radius, 2)
        cos_lat = math.cos(latitude)
        sin_lat = math.sin(latitude)
        numerator = math.pow(er_squared * cos_lat, 2) + math.pow(pr_squared * sin_lat, 2)
        denominator = math.pow(equatorial_radius * cos_lat, 2) + math.pow(polar_radius * sin_lat, 2)
        radius = math.sqrt(numerator / denominator)
        return radius

    @staticmethod
    def lat_long_to_xyz(lat, long, compute_radius=None):
        if not compute_radius:
            raise ValueError('Need to specify method for computing radius')
        radius = compute_radius(lat)
        cos_lat = math.cos(lat)
        x = radius * cos_lat * math.cos(long)
        y = radius * cos_lat * math.sin(long)
        z = radius * math.sin(lat)
        return x, y, z

    @staticmethod
    def xyz_distance(x1, y1, z1, x2, y2, z2):
        x_diff = x1 - x2
        y_diff = y1 - y2
        z_diff = z1 - z2
        return math.sqrt(math.pow(x_diff, 2) + math.pow(y_diff, 2) + math.pow(z_diff, 2))

    def keerthana(self, units='metric'):
        """
        Use Keerthana's algorithm for computing geo distance on this pair.
        :return: float distance in specified units, default is km.
        """
        # Do all calculations using km. Convert at the end if necessary.
        lat1, long1 = self.coord_1.convert_to_radians()
        lat2, long2 = self.coord_2.convert_to_radians()
        x1, y1, z1 = GeoDistance.lat_long_to_xyz(
            lat1,
            long1,
            compute_radius=GeoDistance.keerthana_compute_radius)
        x2, y2, z2 = GeoDistance.lat_long_to_xyz(
            lat2,
            long2,
            compute_radius=GeoDistance.keerthana_compute_radius)
        distance =  GeoDistance.xyz_distance(x1, y1, z1, x2, y2, z2)
        if units != 'metric':
            distance *= self.miles_per_km
        return distance
