import adafruit_tca9548a
from i2c_manager import i2c

tca = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
print("TCA9548A presente en 0x70")  # si esto no da error, el TCA responde