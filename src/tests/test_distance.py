import adafruit_vl53l0x
from utils.i2c_manager import i2c
import libs.GPIO as GPIO
import time

sensor = adafruit_vl53l0x.VL53L0X(i2c)

while True:
    print("Distance: {} mm".format(sensor.range))
    time.sleep(0.5)