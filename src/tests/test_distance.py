import board
import busio
import adafruit_vl53l1x
import time

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l1x.VL53L1X(i2c)

vl53.distance_mode = 2   # 1=short, 2=long
vl53.timing_budget = 200 # ms

while True:
    if vl53.data_ready:
        print("Distance: {} mm".format(vl53.distance))
        vl53.clear_interrupt()
        time.sleep(0.1)
