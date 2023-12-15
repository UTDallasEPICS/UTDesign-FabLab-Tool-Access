#!/bin/bash

# Simulate systemd service behavior
export DISPLAY=:0
export XAUTHORITY=/home/pi/.Xauthority

# Add any other environment variables or configurations as needed

# Run your startup script
/bin/bash /app/startup_script.sh
