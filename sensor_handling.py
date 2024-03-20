# sensor_handling.py
import logging
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)
from dronekit import Vehicle

logs_dir = '/mnt/itamarusb/RSH/logs'

# Setup basic logging
logger = logging.getLogger('sensor_handling')
handler = logging.FileHandler(f'{logs_dir}/sensor_handling.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class SensorHandler:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def get_location(self):
        try:
            return {
                'latitude': self.vehicle.location.global_frame.lat,
                'longitude': self.vehicle.location.global_frame.lon
            }
        except Exception as e:
            logger.error("Failed to get location: %s", e)
            return None

    def get_altitude(self):
        try:
            return self.vehicle.location.global_relative_frame.alt
        except Exception as e:
            logger.error("Failed to get altitude: %s", e)
            return None

    def get_battery_status(self):
        try:
            return self.vehicle.battery
        except Exception as e:
            logger.error("Failed to get battery status: %s", e)
            return None

    def get_velocity(self):
        try:
            return self.vehicle.velocity
        except Exception as e:
            logger.error("Failed to get velocity: %s", e)
            return None

    def get_heading(self):
        try:
            return self.vehicle.heading
        except Exception as e:
            logger.error("Failed to get heading: %s", e)
            return None

    def collect_all_data(self):
        try:
            return {
                'location': self.get_location(),
                'altitude': self.get_altitude(),
                'battery_status': self.get_battery_status(),
                'velocity': self.get_velocity(),
                'heading': self.get_heading()
            }
        except Exception as e:
            logger.error("Failed to collect sensor data: %s", e)
            return {}