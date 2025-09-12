import adafruit_vl53l0x
from utils.tca_manager import tca

class DistanceSensor:
    def __init__(self, tca_channel):
        self.sensor = adafruit_vl53l0x.VL53L0X(tca[tca_channel])

    def get_distance(self):
        if self.sensor is None:
            return 0
        return self.sensor.range