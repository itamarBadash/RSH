# Use an official Python runtime as a parent image, ensure compatibility with ARM architecture
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies for serial communication
RUN apt-get update && apt-get install -y \
    libserialport0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir dronekit pymavlink pyserial

# Since your Python script is on a USB device, you won't copy it into the image. Instead, you'll mount the USB device when you run the container.

# Set the path to your drone handler script
# Note: This will be overridden by the command you use to run the container, as the file is on the USB device.
CMD ["python", "./drone_handler.py"]