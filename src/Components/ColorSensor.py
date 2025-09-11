import adafruit_tcs34725
from utils.i2c_manager import i2c
import threading

class ColorSensor:
    def __init__(self):
        self.sensor = adafruit_tcs34725.TCS34725(i2c)
        self.sensor.integration_time = 24
        self.sensor.gain = 4
        self.thread = None
        self.color = (0, 0, 0, 0)
        self.temp = 0
        self.lux = 0
    
    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self.thread_function, daemon=True)
            self.thread.start()
        else:
            if not self.thread.is_alive():
                self.thread.start()
                return
            print("Color sensor thread already running")
    
    def thread_function(self):
        while True:
            (r, g, b, c), temp, lux = self.get_color()
            self.color = (r, g, b, c)
            self.temp = temp
            self.lux = lux
    
    def get_color(self):
        r, g, b, c = self.sensor.color_raw
        temp = self.sensor.color_temperature
        lux = self.sensor.lux
        return (r, g, b, c), temp, lux