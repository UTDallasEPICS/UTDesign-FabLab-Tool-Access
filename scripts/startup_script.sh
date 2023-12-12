#!/bin/bash

sleep 30 # wait for desktop to load

cd /home/pi/Desktop #Change path accordingly to script location
lxterminal -e python3 script.py > /home/pi/Desktop/script_log.txt 2>&1
