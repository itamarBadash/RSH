import pygame
import sys
import serial

def initialize_pygame():
    pygame.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        print(f"Detected joystick: {joystick.get_name()}")
    if not joysticks:
        print("No joystick detected.")
        sys.exit()
    return joysticks

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def joystick_position_to_pwm(value):
    return clamp(int((value + 1) * 500 + 1000), 1000, 2000)

def broadcast_pwm_to_serial(ser, channel, pwm_value):
    message = f"Channel {channel}: PWM {pwm_value}\n".encode()
    ser.write(message)

def wait_for_acknowledgment(ser):
    print("Waiting for acknowledgment...")
    while True:
        if ser.in_waiting > 0:
            ack = ser.readline().decode().strip()
            if ack == "ACK":
                print("Acknowledgment received.")
                break
            else:
                print("Unexpected response:", ack)
                break

def main():
    joysticks = initialize_pygame()
    ser = serial.Serial("/dev/ttyUSB0", 57600, timeout=1)

    axis_names = {
        0: "Left Stick Horizontal (X-axis)",
        1: "Left Stick Vertical (Y-axis)",
        2: "Right Stick Horizontal (Z-axis)",
        3: "Right Stick Vertical (R-axis)"
    }

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    axis_name = axis_names.get(event.axis, f"Axis {event.axis}")
                    pwm_value = joystick_position_to_pwm(event.value)
                    broadcast_pwm_to_serial(ser, event.axis + 1, pwm_value)
                    print(f"Joystick {event.joy}, {axis_name} moved. PWM: {pwm_value}")
                    wait_for_acknowledgment(ser)
            pygame.time.wait(10)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        ser.close()
        pygame.quit()

if __name__ == "__main__":
    main()
