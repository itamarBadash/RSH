# drone_data_service.py
import threading
import time

class DroneDataService(threading.Thread):
    def __init__(self, vehicle, data, update_interval=1):
        super(DroneDataService, self).__init__()
        self.vehicle = vehicle
        self.data = data
        self.update_interval = update_interval
        self.running = False

    def run(self):
        self.running = True
        try:
            while self.running:
                self.update_data()
                time.sleep(self.update_interval)
        finally:
            print("Data service stopped.")

    def update_data(self):
        self.data['altitude'] = self.vehicle.location.global_relative_frame.alt
        self.data['speed'] = self.vehicle.groundspeed
        self.data['location'] = (self.vehicle.location.global_frame.lat, self.vehicle.location.global_frame.lon)
        self.data['mode'] = self.vehicle.mode.name

    def stop(self):
        self.running = False
