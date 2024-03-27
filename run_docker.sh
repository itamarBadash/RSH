#!/bin/bash
docker run --device=/dev/serial0 --device=/dev/ttyUSB0 -v /mnt/itamarusb/RSH/drone_program:/app -v /mnt/itamarusb/RSH/logs:/mnt/itamarusb/RSH/logs drone-app python3 /app/drone_handler.py
