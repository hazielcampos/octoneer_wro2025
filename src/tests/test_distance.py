import VL53L0X

import time

tof = VL53L0X.VL53L0X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)

while True:
    distance = tof.get_distance()
    print("Distance: {} mm".format(distance))