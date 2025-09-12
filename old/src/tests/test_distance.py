from Components.DistanceSensor import DistanceSensor
from utils.i2c_manager import i2c
import time
import adafruit_tca9548a
import adafruit_tcs34725

tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)

tcs = adafruit_tcs34725.TCS34725(tca[0])
time.sleep(0.1)
sensor_right = DistanceSensor(tca[1])
time.sleep(0.1)
sensor_left = DistanceSensor(tca[2])

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