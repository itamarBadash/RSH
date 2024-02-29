import time
import serial
# Set the serial port and baud rate
serial_port = "/dev/ttyUSB0"  # Change this to match your serial port
baud_rate = 57600  # Baud rate of the SiK radio module

# Open the serial port
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def send_message(message):
    # Encode message to bytes and send it
    ser.write(message.encode('utf-8'))
    print("Message sent:", message)


def receive_acknowledgment():
    # Read from serial port and check for acknowledgment
    acknowledgment = ser.readline().decode('utf-8').strip()
    return acknowledgment


try:
    while True:
        # Input a message from the user to send
        message = input("Enter message to transmit: ")

        # Send the message
        send_message(message)

        # Wait for acknowledgment
        acknowledgment = receive_acknowledgment()
        print("Acknowledgment received:", acknowledgment)

        # Add a small delay
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial port when the program is terminated
    ser.close()
    print("\nProgram terminated. Serial port closed.")
