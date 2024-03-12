import threading
import serial
import time
import re  # Import regular expressions module

class SerialListener:
    def __init__(self, port, baud):
        self.serial_port = serial.Serial(port, baud, timeout=0)
        self.thread = threading.Thread(target=self.listen)
        self.running = False
        self.pwm_values = {}  # Dictionary to store PWM values, keyed by channel

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
                self.process_data(data)

    def process_data(self, data):
        # Assuming data format "Channel X: PWM Y"
        match = re.search(r"Channel (\d+): PWM (\d+)", data)
        if match:
            channel = int(match.group(1))
            pwm = int(match.group(2))
            self.pwm_values[channel] = pwm
            #print(f"Channel {channel}: PWM {pwm} stored")

    def get_pwm_value(self, channel):
        """Return the PWM value for a given channel."""
        return self.pwm_values.get(channel, None)

    def get_all_pwm_values(self):
        """Return all stored PWM values."""
        return self.pwm_values


