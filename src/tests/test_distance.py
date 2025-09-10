import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

addr = 0x29
buf = bytearray(1)
i2c.writeto_then_readfrom(addr, bytes([0xC0]), buf)  # registro de identificación
print("Sensor ID:", hex(buf[0]))

i2c.unlock()
