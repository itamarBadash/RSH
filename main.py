import sys
import time

from connect_to_vehicle import vehicle
try:

    while True:
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Closing the vehicle...")
    vehicle.close()
    print("Closed the vehicle.")