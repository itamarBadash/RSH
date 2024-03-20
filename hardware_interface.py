import logging
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)

from dronekit import VehicleMode, Command
from pymavlink import mavutil


logs_dir = '/mnt/itamarusb/RSH/logs'

# Setup basic logging
# Setup dedicated logger for the module, e.g., 'drone_handler'
logger = logging.getLogger('hardware_interface')
handler = logging.FileHandler(f'{logs_dir}/hardware_interface.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

class HardwareInterface:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def set_flight_mode(self, mode_name):
        try:
            logger.info(f"Changing flight mode to {mode_name}")
            self.vehicle.mode = VehicleMode(mode_name)
        except Exception as e:
            logger.error(f"Failed to change flight mode to {mode_name}: {e}")

    def takeoff(self, altitude):
        try:
            logger.info(f"Taking off to altitude {altitude} meters")
            self.vehicle.simple_takeoff(altitude)
        except Exception as e:
            logger.error(f"Takeoff failed: {e}")

    def goto_location(self, lat, lon, altitude):
        try:
            logger.info(f"Going to location: lat {lat}, lon {lon}, altitude {altitude}")
            cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                          mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                          0, 0, 0, 0, 0, 0, lat, lon, altitude)
            self.vehicle.commands.clear()
            self.vehicle.commands.add(cmd)
            self.vehicle.commands.upload()
            self.vehicle.mode = VehicleMode("AUTO")
        except Exception as e:
            logger.error(f"Failed to go to location: {e}")

    def control_camera(self, tilt, pan):
        # Assuming specific implementation details for camera control are not provided
        logger.info(f"Adjusting camera tilt to {tilt} and pan to {pan}")

    def set_servo_pwm(self, channel, pwm_value):
        try:
            if channel < 1 or channel > 16:
                logger.warning("Channel number must be between 1 and 16.")
                return False

            if pwm_value < 1000 or pwm_value > 2000:
                logger.warning("PWM value must be between 1000 and 2000.")
                return False

            msg = self.vehicle.message_factory.command_long_encode(
                0, 0,  # target system, target component
                mavutil.mavlink.MAV_CMD_DO_SET_SERVO,  # command
                0,  # confirmation
                channel,  # param 1: servo number
                pwm_value,  # param 2: PWM value
                0, 0, 0, 0, 0  # params 3-7 not used
            )
            self.vehicle.send_mavlink(msg)
            logger.info(f"Set servo {channel} to PWM {pwm_value}")
            return True
        except Exception as e:
            logger.error(f"Failed to set servo {channel} to PWM {pwm_value}: {e}")
            return False
