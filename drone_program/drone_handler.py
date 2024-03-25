import logging
import serial
import time
import re
import sys
import os
from pymavlink import mavutil
import configparser


if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)

from dronekit import connect
from hardware_interface import HardwareInterface
from telemetry_service import TelemetryService
from sensor_handling import SensorHandler

config = configparser.ConfigParser()

config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

logs_dir = config['General']['LogsDir']
vehicle_connection_string = config['Connection']['VehicleConnectionString']
vehicle_baud_rate = int(config['Connection']['VehicleBaudRate'])
ground_station_serial_port = config['Connection']['GroundStationSerialPort']
ground_station_baud_rate = int(config['Connection']['GroundStationBaudRate'])

logger = logging.getLogger('drone_handler')
handler = logging.FileHandler(f'{logs_dir}/drone_handler.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


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
        if not match:
            raise ValueError("Invalid command format")

        channel, pwm_value = map(int, match.groups())
        if not (1 <= channel <= 16):
            raise ValueError(f"Channel {channel} out of range. Must be 1-16.")
        if not (1000 <= pwm_value <= 2000):
            raise ValueError(f"PWM {pwm_value} out of range. Must be 1000-2000.")

        success = hardware_interface.set_servo_pwm(channel, pwm_value)
        if not success:
            raise RuntimeError(f"Failed to set channel {channel} to PWM {pwm_value}")
        logger.info(f"Set channel {channel} to PWM {pwm_value}")
        return "ACK\n"
    except ValueError as e:
        logger.warning(f"Validation error for command '{command}': {e}")
        return "NACK\n"
    except Exception as e:
        logger.error(f"Unexpected error processing command '{command}': {e}")
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
