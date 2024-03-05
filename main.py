import time
import sys
from serial_listener import listener
try:
    while True:

        time.sleep(0.1)

except KeyboardInterrupt:
    listener.stop()