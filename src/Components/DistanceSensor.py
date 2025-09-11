import adafruit_vl53l0x
import libs.GPIO as GPIO
import time

class DistanceSensor:
    def __init__(self, i2c):
        self.i2c = i2c
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)

    def get_distance(self):
        if self.sensor is None:
            return 0
        return self.sensor.range