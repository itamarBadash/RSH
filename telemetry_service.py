# telemetry_service.py
import logging
import threading
import time
from sensor_handling import SensorHandler

logs_dir = '/mnt/itamarusb/RSH/logs'

# Setup basic logging
logger = logging.getLogger('telemetry_service')
handler = logging.FileHandler(f'{logs_dir}/telemetry_service.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
class TelemetryService(threading.Thread):
    def __init__(self, vehicle, update_interval=1):
        threading.Thread.__init__(self)
        self.vehicle = vehicle
        self.update_interval = update_interval
        self.sensor_handler = SensorHandler(vehicle)
        self.telemetry_data = {}
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            try:
                self.update_telemetry()
            except Exception as e:
                logger.error(f"Error updating telemetry: {e}")
            time.sleep(self.update_interval)

    def update_telemetry(self):
        # Collects telemetry data from the drone and updates the telemetry_data dictionary.
        try:
            self.telemetry_data['location'] = self.sensor_handler.get_location()
            self.telemetry_data['altitude'] = self.sensor_handler.get_altitude()
            self.telemetry_data['battery'] = self.sensor_handler.get_battery_status()
            self.telemetry_data['velocity'] = self.sensor_handler.get_velocity()
            self.telemetry_data['heading'] = self.sensor_handler.get_heading()
        except Exception as e:
            logger.error(f"Failed to update telemetry data: {e}")
            raise

    def get_telemetry(self):
        return self.telemetry_data

    def stop(self):
        self.running = False