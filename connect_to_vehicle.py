import time
import sys
if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)

import dronekit

def mode_callback(self, attribute_name, message):
    print(self.mode.name)


def parameter_callback(self, parameter_name, message):
    print(parameter_name, message)


def message_callback(self, message_name, message):
    print("Heartbeat:", self.last_heartbeat)
def connect_to_drone():
    # MAVProxy serial connection string
    connection_string = '/dev/ttyUSB0'  # Modify this according to your setup

    try:
        print("Connecting to the drone...")
        vehicle = dronekit.connect(ip="127.0.0.1:14550", wait_ready=True)
        vehicle.add_message_listener("HEARTBEAT", message_callback)
        return vehicle
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# Main function
connected = False
retry_interval = 10 # Retry interval in seconds

while not connected:
    vehicle = connect_to_drone()
    if vehicle is not None:
        connected = True
        print('connected to vehicle!')

    else:
        print(f"Retrying connection in {retry_interval} seconds...")
        time.sleep(retry_interval)


def get_vehicle():
    return vehicle
