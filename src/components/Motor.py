import Rasp.GPIO as GPIO
import time

last_speed = 0

# =========================
# GPIO setup
# =========================
FORWARD_IO = 12  # GPIO pin to move the motor forward
BACKWARD_IO = 13  # GPIO pin to move the motor backward
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 1000)  #
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 1000)  # 1 kHz
def start():
    FORWARD_PWM.start(0)
    BACKWARD_PWM.start(0)

def forward(speed):
    global last_speed
    if last_speed == 0:
        BACKWARD_PWM.ChangeDutyCycle(0)
        FORWARD_PWM.ChangeDutyCycle(50)
        time.sleep(0.7)
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)
def backward(speed):
    global last_speed
    if last_speed == 0:
        BACKWARD_PWM.ChangeDutyCycle(50)
        FORWARD_PWM.ChangeDutyCycle(0)
        time.sleep(0.7)
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)
def stop_motors():
    global last_speed
    last_speed = 0
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(0)