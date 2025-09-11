import board, busio, adafruit_tca9548a

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)

tca[0].try_lock()  # abre el canal 0
devices = tca[0].scan()
tca[0].unlock()
print([hex(d) for d in devices])