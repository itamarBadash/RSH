# sensor_handling.py
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)
from dronekit import Vehicle

class SensorHandler:
    def __init__(self, vehicle):
        """
        Initializes the SensorHandler with a vehicle object.
        """
        self.vehicle = vehicle

    def get_location(self):
        """
        Returns the current location of the drone.
        """
        return {
            'latitude': self.vehicle.location.global_frame.lat,
            'longitude': self.vehicle.location.global_frame.lon
        }

    def get_altitude(self):
        """
        Returns the current altitude of the drone.
        """
        return self.vehicle.location.global_relative_frame.alt

    def get_battery_status(self):
        """
        Returns the current battery status.
        """
        return self.vehicle.battery

    def get_velocity(self):
        """
        Returns the current velocity of the drone.
        """
        return self.vehicle.velocity

    def get_heading(self):
        """
        Returns the current heading of the drone.
        """
        return self.vehicle.heading

    def collect_all_data(self):
        """
        Collects and returns all relevant sensor data in a dictionary.
        """
        return {
            'location': self.get_location(),
            'altitude': self.get_altitude(),
            'battery_status': self.get_battery_status(),
            'velocity': self.get_velocity(),
            'heading': self.get_heading()
        }

# Example usage
