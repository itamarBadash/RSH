
import threading
import serial
import time


class SerialListener:
    def __init__(self, port, baud):
        self.serial_port = serial.Serial(port, baud_rate, timeout=0)
        self.thread = threading.Thread(target=self.listen)
        self.running = False

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def listen(self):
        while self.running:
            if self.serial_port.in_waiting:
                data = self.serial_port.readline().decode().strip()
                print(f"Received data: {data}")
                # React to the data here


serial_port = '/dev/ttyUSB0'  # Update this with your serial port
baud_rate = 57600  # Update this with your baud rate

listener = SerialListener(serial_port, baud_rate)
listener.start()