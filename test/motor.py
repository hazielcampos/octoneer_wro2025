
import time
import keyboard


from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

import busio
import board

import Rasp.GPIO as GPIO
import time

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


# =========================
# GPIO setup
# =========================
FORWARD_IO = 12  # GPIO pin to move the motor forward
BACKWARD_IO = 13  # GPIO pin to move the motor backward
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 500)  #
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 500)  # 200 Hz
def start_pwm():
    FORWARD_PWM.start(0)
    BACKWARD_PWM.start(0)

def forward(speed):
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)
def backward(speed):
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)
def stop_motors():
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(0)


speed = 30
def increase_speed(amount):
    global speed
    speed = min(speed + amount, 100)

def decrease_speed(amount):
    global speed
    speed = max(speed - amount, 10)

def main():
    start_pwm()
    while True:
        if keyboard.is_pressed("w"):
            forward(speed)
        elif keyboard.is_pressed("s"):
            backward(speed)
        if keyboard.is_pressed("d"):
            set_angle(RIGHT_POSITION)
        elif keyboard.is_pressed("a"):
            set_angle(LEFT_POSITION)
        else:
            set_angle(CENTER_POSITION)
            
        if keyboard.is_pressed("space"):
            stop_motors()
        if keyboard.is_pressed("e"):
            increase_speed(10)
        elif keyboard.is_pressed("q"):
            decrease_speed(10)
    
try:
    main()
except KeyboardInterrupt:
    stop_motors()
    print("User interrupt")

