import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)