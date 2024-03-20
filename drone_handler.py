import logging
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
from hardware_interface import HardwareInterface
from telemetry_service import TelemetryService
from sensor_handling import SensorHandler

# Setup basic logging
logs_dir = '/mnt/itamarusb/RSH/logs'

# Setup basic logging
logger = logging.getLogger('drone_handler')
handler = logging.FileHandler(f'{logs_dir}/drone_handler.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
# Connection parameters
vehicle_connection_string = '/dev/serial0'
vehicle_baud_rate = 921600
ground_station_serial_port = '/dev/ttyUSB0'
ground_station_baud_rate = 57600

def wait_for_heartbeat(connection):
    logger.info("Waiting for heartbeat from vehicle")
    connection.wait_heartbeat()
    logger.info("Heartbeat from vehicle received")

def connect_via_pymavlink(connection_string):
    logger.info(f"Connecting to drone via {connection_string} with baud rate {vehicle_baud_rate}")
    mavlink_connection = mavutil.mavlink_connection(
        device=connection_string,
        baud=vehicle_baud_rate
    )
    return mavlink_connection

def process_command(command, hardware_interface):
    try:
        match = re.match(r"Channel (\d+): PWM (\d+)", command)
        if match:
            channel, pwm_value = map(int, match.groups())
            success = hardware_interface.set_servo_pwm(channel, pwm_value)
            if success:
                logger.info(f"Set channel {channel} to PWM {pwm_value}")
                return "ACK\n"
            else:
                logger.error(f"Failed to set channel {channel} to PWM {pwm_value}")
                return "NACK\n"
        else:
            logger.error(f"Command format error: {command}")
            return "NACK\n"
    except Exception as e:
        logger.exception(f"Error processing command: {e}")
        return "NACK\n"

def main():
    logger.info("Connecting to drone...")
    try:
        vehicle = connect(vehicle_connection_string, baud=vehicle_baud_rate, wait_ready=True)
        logger.info("Drone connected")

        hardware_interface = HardwareInterface(vehicle)
        sensor_handler = SensorHandler(vehicle)
        telemetry_service = TelemetryService(vehicle)
        telemetry_service.start()
        logger.info("Telemetry service started")

        ser = serial.Serial(ground_station_serial_port, ground_station_baud_rate, timeout=1)
        logger.info(f"Listening for commands on {ground_station_serial_port}")

        while True:
            if ser.in_waiting > 0:
                command = ser.readline().decode().strip()
                ack = process_command(command, hardware_interface)
                ser.write(ack.encode())

            if time.time() % 5 < 1:
                telemetry_data = telemetry_service.get_telemetry()
                logger.info(f"Telemetry update: {telemetry_data}")
                time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Operation interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        logger.info("Shutting down")
        if 'telemetry_service' in locals():
            telemetry_service.stop()
            telemetry_service.join()
        if 'ser' in locals():
            ser.close()
        if 'vehicle' in locals():
            vehicle.close()
        logger.info("Shutdown complete")

if __name__ == "__main__":
    main()