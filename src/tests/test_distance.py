from Components.DistanceSensor import DistanceSensor
import time

sensor_right = DistanceSensor(xshut_pin=22, new_address=0x30)
sensor_left = DistanceSensor(xshut_pin=27, new_address=0x31)

sensor_right.init_sensor()
sensor_left.init_sensor()

import Components.ColorSensor as ColorSensor
    
try:
    print("Press Ctrl-C to stop")
    while True:
        print("right: ", sensor_right.get_distance())
        print("left: ",sensor_left.get_distance())
        (r, g, b, c), temp, lux = ColorSensor.sensor_read()
        print(f"R: {r}, G: {g}, B: {b}, C: {c}, Temp: {temp}, Lux: {lux}")
        time.sleep(0.1)
except KeyboardInterrupt:
    sensor_right.sensor.set_address(0x29)
    sensor_left.sensor.set_address(0x29)