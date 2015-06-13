#!/bin/sh
# launcher.sh
# go to home directory and run the script

cd /
cd home/pi/scripts
sudo python auto_off.py &
sudo python cap_sense2.py &
cd /
