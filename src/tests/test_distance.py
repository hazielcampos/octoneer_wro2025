import adafruit_vl53l0x
from utils.i2c_manager import i2c
import libs.GPIO as GPIO

import time

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)   # Enciende el sensor
time.sleep(0.05)

sensor = adafruit_vl53l0x.VL53L0X(i2c)
time.sleep(0.1)

while True:
    print("Distance: {} mm".format(sensor.range))
    time.sleep(0.5)