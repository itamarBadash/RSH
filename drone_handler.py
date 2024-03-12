import time
import serial
import dronekit
import re


def connect_to_drone(connection_string, baud_rate):
    try:
        print("Connecting to the drone...")
        vehicle = dronekit.connect(connection_string, baud=baud_rate, wait_ready=True)
        print("Connected to vehicle!")
        return vehicle
    except Exception as e:
        print(f"Connection failed: {e}")
        exit()


def process_command_and_acknowledge(ser, command, vehicle):
    # Parse the command
    match = re.match(r"Channel (\d+): PWM (\d+)", command)
    if match:
        channel, pwm = int(match.group(1)), int(match.group(2))
        if 1 <= channel <= 8:  # Assuming channels 1-8 are valid
            # Update the vehicle channel override
            vehicle.channels.overrides[str(channel)] = pwm
            print(f"Set channel {channel} to PWM {pwm}")
            # Send an acknowledgment
            ser.write(b"ACK\n")
        else:
            print("Invalid channel:", channel)
            ser.write(b"NACK\n")  # Negative acknowledgment for invalid channel
    else:
        print("Command format error:", command)
        ser.write(b"NACK\n")  # Negative acknowledgment for format error


def main():
    # Replace these with your actual drone connection details
    connection_string = '/dev/serial0'
    baud_rate = 921600

    # Replace with your actual serial port details for receiving commands
    serial_port = '/dev/ttyUSB0'
    serial_baud_rate = 57600

    vehicle = connect_to_drone(connection_string, baud_rate)
    ser = serial.Serial(serial_port, serial_baud_rate, timeout=1)

    try:
        while True:
            if ser.in_waiting > 0:
                command = ser.readline().decode().strip()
                process_command_and_acknowledge(ser, command, vehicle)
            time.sleep(0.1)  # Adjust as needed
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        ser.close()
        if vehicle is not None:
            vehicle.close()


if __name__ == "__main__":
    main()
