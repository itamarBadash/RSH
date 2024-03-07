import pygame
import sys
import serial


def broadcast_pwm_to_serial(port, baud_rate, channel, pwm_value):
    """
    Send a PWM value for a specific channel to a serial port.

    Parameters:
    - port: The serial port to use (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux).
    - baud_rate: The baud rate for the serial communication.
    - channel: The channel number to which the PWM value applies.
    - pwm_value: The PWM value to send.
    """
    if not 1 <= channel <= 9:
        raise ValueError("Channel must be between 1 and 9.")

    # Establish a serial connection
    with serial.Serial(port, baud_rate, timeout=1) as ser:
        # Create a message in the desired format
        message = f"Channel {channel}: PWM {pwm_value}\n".encode()

        # Send the message
        ser.write(message)

def clamp(value, min_value, max_value):
    """Ensure value is between min_value and max_value."""
    return max(min_value, min(value, max_value))

# Initialize Pygame
pygame.init()

# Initialize joysticks
joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Detected joystick {i}: {joystick.get_name()}")

if len(joysticks) == 0:
    print("No joystick detected.")
    sys.exit()

def joystick_position_to_pwm(value):
    """
    Convert joystick position (-1 to 1) to PWM value (1000 to 2000).
    Neutral joystick position (0) corresponds to PWM 1500.
    """
    return clamp(int((value + 1) * 500 + 1000), 1000, 2000)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                # Determine which joystick and axis are being used
                joystick_index = event.joy
                if event.axis == 0:
                    axis_name = "Left Stick Horizontal (X-axis)"
                elif event.axis == 1:
                    axis_name = "Left Stick Vertical (Y-axis)"
                elif event.axis == 2:
                    axis_name = "Right Stick Horizontal (Z-axis)"
                elif event.axis == 3:
                    axis_name = "Right Stick Vertical (R-axis)"
                else:
                    axis_name = f"Axis {event.axis}"

                pwm_value = joystick_position_to_pwm(event.value)
                broadcast_pwm_to_serial("/dev/ttyUSB0",57600,1,f"Joystick {joystick_index}, {axis_name} moved. PWM: {pwm_value}")


except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    pygame.quit()
