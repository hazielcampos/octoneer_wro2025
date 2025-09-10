from Components.DistanceSensor import DistanceSensor
import time

sensor_right = DistanceSensor(xshut_pin=22, new_address=0x30)
#sensor_left = DistanceSensor(xshut_pin=27, new_address=0x31)

sensor_right.init_sensor()
#sensor_left.init_sensor()
    
try:
    print("Press Ctrl-C to stop")
    while True:
        print(sensor_right.get_distance())
        time.sleep(0.1)
except KeyboardInterrupt:
    sensor_right.sensor.set_address(0x29)