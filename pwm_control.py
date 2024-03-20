# pwm_control.py
from pymavlink import mavutil

class PWMControl:

    def __init__(self, mavlink_connection):
        """
        Initializes the PWMControl with a MAVLink connection.
        This connection should be a pymavlink connection object,
        allowing direct sending of MAVLink messages.
        """
        self.mavlink_connection = mavlink_connection

    def update_pwm(self, channel, pwm_value):
        """
        Sends a PWM value to a specific channel.
        """
        # Ensure the channel and pwm_value are within acceptable ranges
        if not 1 <= channel <= 8:
            print("Channel out of range. Must be between 1 and 8.")
            return False

        if not 1000 <= pwm_value <= 2000:
            print("PWM value out of range. Must be between 1000 and 2000.")
            return False

        # Preparing an array with only the relevant channel changed
        rc_channel_values = [65535] * 8  # 65535 indicates no change in pymavlink
        rc_channel_values[channel - 1] = pwm_value

        # Sending the PWM override message
        self.mavlink_connection.mav.rc_channels_override_send(
            self.mavlink_connection.target_system,
            self.mavlink_connection.target_component,
            *rc_channel_values)

        print(f"Channel {channel} set to PWM {pwm_value}")
        return True
