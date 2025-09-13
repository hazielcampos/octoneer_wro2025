import Rasp.GPIO as GPIO
import time
# =========================
# GPIO setup
# =========================
FORWARD_IO = 12  # GPIO pin to move the motor forward
BACKWARD_IO = 13  # GPIO pin to move the motor backward
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 500)  #
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 500)  # 200 Hz
def start():
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