import board, busio, adafruit_tca9548a

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c)

if tca[0].try_lock():
    devices = tca[0].scan()
    tca[0].unlock()
    print("Canal 1:", [hex(d) for d in devices])
else:
    print("No se pudo bloquear el canal 0")
