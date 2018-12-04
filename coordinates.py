import math
from _pydecimal import Decimal


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
