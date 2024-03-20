# telemetry_service.py
import threading
import time
from sensor_handling import SensorHandler

class TelemetryService(threading.Thread):
    def __init__(self, vehicle, update_interval=1):
        """
        Initializes the TelemetryService with a vehicle object and an update interval.
        """
        threading.Thread.__init__(self)
        self.vehicle = vehicle
        self.update_interval = update_interval
        self.sensor_handler = SensorHandler(vehicle)
        self.telemetry_data = {}
        self.running = False

    def run(self):
        """
        Starts the telemetry service, collecting and updating data at the specified interval.
        """
        self.running = True
        while self.running:
            self.update_telemetry()
            time.sleep(self.update_interval)

    def update_telemetry(self):
        """
        Collects telemetry data from the drone and updates the telemetry_data dictionary.
        """
        self.telemetry_data['location'] = self.sensor_handler.get_location()
        self.telemetry_data['altitude'] = self.sensor_handler.get_altitude()
        self.telemetry_data['battery'] = self.sensor_handler.get_battery_status()
        self.telemetry_data['velocity'] = self.sensor_handler.get_velocity()
        self.telemetry_data['heading'] = self.sensor_handler.get_heading()

    def get_telemetry(self):
        """
        Returns the latest telemetry data.
        """
        return self.telemetry_data

    def stop(self):
        """
        Stops the telemetry service.
        """
        self.running = False

