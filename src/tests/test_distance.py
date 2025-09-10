from src.Components.DistanceSensor import DistanceSensor
import time

sensor_right = DistanceSensor(xshut_pin=22, new_address=0x30)
sensor_left = DistanceSensor(xshut_pin=27, new_address=0x31)

while True:
    print(sensor_right.get_distance())
    print(sensor_left.get_distance())
    time.sleep(0.001)