import board, busio, adafruit_tca9548a

i2c = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)

print("TCA9548A presente en 0x70")  # si esto no da error, el TCA responde

for ch in range(8):
    if tca[ch].try_lock():
        devices = tca[ch].scan()
        tca[ch].unlock()
        print(f"Canal {ch}: {devices}")
    else:
        print(f"No se pudo bloquear canal {ch}")