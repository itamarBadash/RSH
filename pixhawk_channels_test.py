from connect_to_vehicle import vehicle
import time

def override_channel(channel, pwm_value):
    """
    Overrides a channel with a specified PWM value.

    Args:
    - channel: int, the channel number to override.
    - pwm_value: int, the PWM value to set.
    """
    # Create a dictionary with channel values
    overrides = vehicle.channels.overrides

    # Override the specific channel
    overrides[channel] = pwm_value
    vehicle.channels.overrides = overrides


def wait_for_pwm_change(channel, timeout=10):
    """
    Waits for the PWM value of a channel to change and measures the time until the change.

    Args:
    - channel: int, the channel number to monitor for change.
    - timeout: int, the timeout in seconds before giving up.

    Returns:
    - The time taken for the PWM value to change, or None if it timed out.
    """
    start_time = time.time()
    initial_pwm = vehicle.channels[channel]
    elapsed_time = 0

    while elapsed_time < timeout:
        current_pwm = vehicle.channels[channel]
        if current_pwm != initial_pwm:
            return time.time() - start_time

        time.sleep(0.1)  # Sleep briefly to prevent hammering the check
        elapsed_time = time.time() - start_time

    return None


# Example usage
channel_to_override = 3  # Choose your channel here
pwm_value_to_set = 1500  # Example PWM value

print(f"Overriding channel {channel_to_override} with PWM {pwm_value_to_set}")
override_channel(channel_to_override, pwm_value_to_set)

# Now we wait for the PWM to change and measure the time
print(f"Waiting for PWM on channel {channel_to_override} to change...")
time_taken = wait_for_pwm_change(channel_to_override)

if time_taken is not None:
    print(f"Time taken for PWM change: {time_taken} seconds")
else:
    print("PWM did not change within the timeout period.")

# Clean up by clearing the override
vehicle.channels.overrides = {}
vehicle.close()
