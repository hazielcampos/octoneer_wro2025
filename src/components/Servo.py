from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import busio
import board

i2c = busio.I2C(board.SCL, board.SDA)

CENTER_POSITION = 52  # Neutral position of the servo
LEFT_POSITION = 62 # Left position of the servo
RIGHT_POSITION = 42  # Right position of the servo

# =========================
# PCA9685 and Servo setup
# =========================
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50  # Servo frequency
direction_servo = servo.Servo(pca.channels[0])

def set_angle(angle: float):
    """Set the servo angle."""
    if angle < 42 or angle > 62:
        raise ValueError("Angle must be between 0 and 180 degrees.")
    direction_servo.angle = angle

def disable():
    pca.deinit()  # Deinitialize PCA9685