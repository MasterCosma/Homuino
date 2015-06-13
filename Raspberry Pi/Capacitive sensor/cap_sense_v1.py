import capacitive
import time

millis = lambda: int(round(time.time() * 1000))
threshold = 300
count = 0
previousMillis = 0

while True:
    cap1 = capacitive.CapRead(26, 13)
    cap2 = capacitive.CapRead(19, 13)
    if cap1 > threshold :
        previousMillis = millis()
        count = millis() - previousMillis
        print("Ciao")
        while count < 500:
            count = millis() - previousMillis
            cap2 = capacitive.CapRead(19, 13)
            if cap2 > threshold:
                if count < 100:
                    #CLICK
                else :
                    #SWIPE
