import time
import board
import os
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D6, echo_pin=board.D19)

while True:
    try:
        print((sonar.distance,))
        if ((sonar.distance < 10) and (sonar.distance>1)):
            fifo = open("/home/pi/SONAR_FIFO.fifo", "w")
            fifo.write("1")
            fifo.close()
        else:
            fifo = open("/home/pi/SONAR_FIFO.fifo", "w")
            fifo.write("0")
            fifo.close()
        
    except RuntimeError:
        print("Retrying!")
    time.sleep(1)
