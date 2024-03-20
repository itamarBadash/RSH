import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    import collections
    from collections.abc import MutableMapping
    setattr(collections, "MutableMapping", MutableMapping)

from dronekit import VehicleMode, Command
from pymavlink import mavutil


class HardwareInterface:
    def __init__(self, vehicle):
        """
        Initializes the HardwareInterface with a vehicle object.
        """
        self.vehicle = vehicle

    def set_flight_mode(self, mode_name):
        """
        Sets the vehicle's flight mode.
        """
        print(f"Changing flight mode to {mode_name}")
        self.vehicle.mode = VehicleMode(mode_name)

    def takeoff(self, altitude):
        """
        Commands the vehicle to take off to a specified altitude.
        """
        print(f"Taking off to altitude {altitude} meters")
        self.vehicle.simple_takeoff(altitude)  # DroneKit's simple_takeoff method

    def goto_location(self, lat, lon, altitude):
        """
        Commands the vehicle to go to a specified latitude, longitude, and altitude.
        """
        print(f"Going to location: lat {lat}, lon {lon}, altitude {altitude}")
        location = mavutil.mavlink.MAVLink_mission_item_message(
            self.vehicle.target_system, self.vehicle.target_component,
            0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0, 0, 0, 0, 0, 0,
            lat, lon, altitude)
        cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                      mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                      0, 0, 0, 0, 0, 0, lat, lon, altitude)
        self.vehicle.commands.clear()
        self.vehicle.commands.add(cmd)
        self.vehicle.commands.upload()
        self.vehicle.mode = VehicleMode("AUTO")

    def control_camera(self, tilt, pan):
        """
        Adjusts the camera's tilt and pan.
        """
        print(f"Adjusting camera tilt to {tilt} and pan to {pan}")
        # Example: Sending MAVLink messages to control camera gimbal
        # This method needs to be implemented based on your camera gimbal's specifics.

    def set_servo_pwm(self, channel, pwm_value):
        """
        Sets the PWM value of a servo.

        :param channel: The channel number of the servo (usually 1 to 8 on Pixhawk)
        :param pwm_value: The PWM value to set (usually between 1000 and 2000)
        """
        if channel < 1 or channel > 16:
            print("Channel number must be between 1 and 16.")
            return False

        if pwm_value < 1000 or pwm_value > 2000:
            print("PWM value must be between 1000 and 2000.")
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
        print(f"Set servo {channel} to PWM {pwm_value}")
        return True
