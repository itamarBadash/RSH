import serial
import time
import re
import sys
from pymavlink import mavutil


if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)

from dronekit import connect
from mavlink_comm import MAVLinkComm
from hardware_interface import HardwareInterface
from telemetry_service import TelemetryService
from pwm_control import PWMControl
from sensor_handling import SensorHandler


# Connection parameters
vehicle_connection_string = '/dev/serial0'
vehicle_baud_rate = 921600
ground_station_serial_port = '/dev/ttyUSB0'
ground_station_baud_rate = 57600
def wait_for_heartbeat(connection):
    print("Waiting for heartbeat from vehicle")
    connection.wait_heartbeat()
    print("Heartbeat from vehicle received")
def connect_via_pymavlink(connection_string):
    """
    Establishes a connection to the drone using pymavlink.

    Parameters:
    - connection_string: String representing the connection path (e.g., serial port, UDP endpoint).
    - baud: Baud rate for serial connections. Ignored for UDP connections.
    - source_system: Source system ID for this connection, useful in multi-vehicle setups or advanced configurations.

    Returns:
    - mavlink_connection: A MAVLink connection object.
    """
    print(f"Connecting to drone via {connection_string} with baud rate {vehicle_baud_rate}")
    mavlink_connection = mavutil.mavlink_connection(
        device=connection_string,
        baud=vehicle_baud_rate
    )


def process_command(command, hardware_interface):
    """
    Process incoming command from the ground station and execute it.
    """
    match = re.match(r"Channel (\d+): PWM (\d+)", command)
    if match:
        channel, pwm_value = map(int, match.groups())
        # Ensure pwm_control is correctly using a method to send PWM commands
        success = hardware_interface.set_servo_pwm(channel, pwm_value)
        if success:
            print(f"Set channel {channel} to PWM {pwm_value}")
            return "ACK\n"
        else:
            return "NACK\n"
    else:
        print(f"Command format error: {command}")
        return "NACK\n"

def main():
    print("Connecting to drone...")
    vehicle = connect(vehicle_connection_string, baud=vehicle_baud_rate, wait_ready=True)
    print("Drone connected")

    hardware_interface = HardwareInterface(vehicle)
    sensor_handler = SensorHandler(vehicle)
    telemetry_service = TelemetryService(vehicle)
    telemetry_service.start()
    print("Telemetry service started")

    # Setup serial communication with the ground station
    ser = serial.Serial(ground_station_serial_port, ground_station_baud_rate, timeout=1)
    print(f"Listening for commands on {ground_station_serial_port}")

    try:
        while True:
            if ser.in_waiting > 0:
                command = ser.readline().decode().strip()
                ack = process_command(command, hardware_interface)
                ser.write(ack.encode())

            # Example telemetry update
            if time.time() % 5 < 1:
                telemetry_data = telemetry_service.get_telemetry()
                print(telemetry_data)
                time.sleep(1)

    except KeyboardInterrupt:
        print("Operation interrupted by user")

    finally:
        print("Stopping telemetry service")
        telemetry_service.stop()
        telemetry_service.join()
        ser.close()
        print("Closing vehicle connection")
        vehicle.close()
        print("Shutdown complete")

if __name__ == "__main__":
    main()