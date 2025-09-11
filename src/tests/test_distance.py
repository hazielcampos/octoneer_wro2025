from Components.DistanceSensor import DistanceSensor
from utils.i2c_manager import i2c
import time
import adafruit_tca9548a
import adafruit_tcs34725

sensor_right = DistanceSensor(xshut_pin=22, new_address=0x30)
sensor_left = DistanceSensor(xshut_pin=27, new_address=0x31)

sensor_right.init_sensor()
sensor_left.init_sensor()
time.sleep(0.1)

tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
tcs = adafruit_tcs34725.TCS34725(tca[0])

tcs.integration_time = 200
tcs.gain = 4

try:
    print("Press Ctrl-C to stop")
    while True:
        r, g, b, c = tcs.color_raw
        color_temp = tcs.color_temperature
        lux = tcs.lux
        
        print("Color: ({0}, {1}, {2}, {3})".format(r, g, b, c))
        print("Color Temperature: {0} K".format(color_temp))
        print("Luminosity: {0} Lux".format(lux))
        print("right: ", sensor_right.get_distance())
        print("left: ",sensor_left.get_distance())
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopped by User")
finally:
    sensor_right.sensor.set_address(0x29)
    sensor_left.sensor.set_address(0x29)