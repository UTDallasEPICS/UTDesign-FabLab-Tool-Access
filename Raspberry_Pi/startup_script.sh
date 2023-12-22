#!/bin/bash

# wait for desktop to load
sleep 20 

# Change path accordingly to script location
cd /home/pi/Desktop/UTDesign-FabLab-Tool-Access/Raspberry_Pi
xterm -e python3 FabFivePi.py > /home/pi/Desktop/UTDesign-FabLab-Tool-Access/Raspberry_Pi/script_log.txt 2>&1
