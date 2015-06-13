# Script made by Cosma Vergari - 2015
#
# It consists in a value check routine for two capacitive foils connected to GPIO
# A ltr swipe means next song, while a rtl swipe means previous song
# A long press on one side means to toggle something depending on which side
# The values are configured for two 4x8cm fold aluminum foils along with 2x 1MOhm resistors
#
# This script outputs its commands through a text file called "action" in the same folder

import capacitive  # Inspired by arduino library CapacitiveSensor's CapacitiveSensor.cpp
import time

millis = lambda: int(round(time.time() * 1000))  # Function similiar to Arduino's millis()
sendPin = 13    # Send pin in common for the two receive pins
receivePin1 = 26  #  Receive pins       WARNING:Must use GPIO.BCM scheme for pin declaration
receivePin2 = 16
threshold = 300   # Minimum capacitance value before action
count = 0         # Will come in handy later
previousMillis = 0   # Will come in handy later
tick0 = 0   # Counter for cap1
tick1 = 0   # Counter for cap2

while True:
	cap1 = capacitive.CapRead(receivePin1, sendPin)  # Read capacitance values
	cap2 = capacitive.CapRead(receivePin2, sendPin)

	if cap1 > threshold :   # cap1 pressed
		previousMillis = millis()    # some timing stuff so as to count 500ms before giving results
		count = millis() - previousMillis 
		while count < 500:
			count = millis() - previousMillis
			cap2 = capacitive.CapRead(receivePin2, sendPin)  # Refresh cap2 value in order to intercept a possible swipe

			if cap2 > threshold and count > 100:  # if cap2 pressed and 100ms elapsed
                open("action", 'w+').write("previousMPD$0")   # go to previous song
				time.sleep(1)  # A bit of rest
				tick0 = 0   # reset counter
				break
			else:
				tick0 += 1   # if the swipe control timeouts...
		if tick0 > 2000:    # ...the counter is over 2000...
			open("action", 'w+').write("toggleMPD$0")  # ...and it is considered as a button pressed -> toggle play/pause
		tick0 = 0   # reset the counter
	else:
		if cap2 > threshold:  # same thing over here...
			previousMillis = millis()
			count = millis() - previousMillis
			while count < 500:
				count = millis() - previousMillis
				cap1 = capacitive.CapRead(receivePin1, sendPin)
				if cap1 > threshold and count > 100:
					open("action", 'w+').write("nextMPD$0")
					time.sleep(1)
					tick1 = 0
					break
				else:
					tick1 += 1
			if tick1 > 2000:
				open("action", 'w+').write("disable$0") # Here the button pressed is used to toggle stereo auto shutdown
			tick1 = 0
