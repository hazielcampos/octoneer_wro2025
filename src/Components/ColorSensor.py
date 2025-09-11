import adafruit_tcs34725
from utils.tca_manager import tca

class ColorSensor:
    def __init__(self, tca_channel):
        self.sensor = adafruit_tcs34725.TCS34725(tca[tca_channel])
        self.sensor.integration_time = 24
        self.sensor.gain = 4
    
    def get_color(self):
        r, g, b, c = self.sensor.color_raw
        temp = self.sensor.color_temperature
        lux = self.sensor.lux
        return (r, g, b, c), temp, lux