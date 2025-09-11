import board, busio, adafruit_tca9548a
import adafruit_tcs34725
import adafruit_vl53l0x
import time

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)

print("TCA9548A presente en 0x70")  # si esto no da error, el TCA responde
tcs = adafruit_tcs34725.TCS34725(tca[0])

tcs.integration_time = 24
tcs.gain = 4

vlx = adafruit_vl53l0x.VL53L0X(tca[1])

try:
    print("Press Ctrl-C to stop")
    while True:
        r, g, b, c = tcs.color_raw
        color_temp = tcs.color_temperature
        lux = tcs.lux
        
        print("Color: ({0}, {1}, {2}, {3})".format(r, g, b, c))
        print("Color Temperature: {0} K".format(color_temp))
        print("Luminosity: {0} Lux".format(lux))
        print("Distance: {} mm".format(vlx.range))
except KeyboardInterrupt:
    print("Stopped by User")