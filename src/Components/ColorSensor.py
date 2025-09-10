from utils.i2c_manager import i2c
import adafruit_tcs34725

sensor = adafruit_tcs34725.TCS34725(i2c)

sensor.integration_time = 100
sensor.gain = 4

def sensor_read():
    r, g, b, c = sensor.color_raw
    temp = sensor.color_temperature
    lux = sensor.lux
    return (r, g, b, c), temp, lux