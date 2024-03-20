import time
import sys
from connect_to_vehicle import vehicle
from connect_to_vehicle import message_callback
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    # vehicle.remove_attribute_listener("mode", mode_callback)
    # vehicle.parameters.remove_attribute_listener("SYSID_THISMAV", parameter_callback)
    vehicle.remove_message_listener("HEARTBEAT", message_callback)
    print("Closing the vehicle...")
    vehicle.close()
    print("Closed the vehicle.")