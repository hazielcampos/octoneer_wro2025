import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO
from libs import betterTime as time2
import threading
import time

from SensorsManager import line_position

# =========================
# Constants
# =========================
CENTER_POSITION = 42  # Neutral position of the servo
LEFT_POSITION = 32 # Left position of the servo
RIGHT_POSITION = 52  # Right position of the servo

# =========================
# State variables
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active

# =========================
# PCA9685 and Servo setup
# =========================
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Servo frequency
direction_servo = servo.Servo(pca.channels[0])

# =========================
# GPIO setup
# =========================
FORWARD_IO = 12  # GPIO pin to move the motor forward
BACKWARD_IO = 13  # GPIO pin to move the motor backward
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 1000)  #
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 1000)  # 1 kHz

def forward(speed):
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)
def backward(speed):
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)
def stop_motors():
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(0)

Kp = 30.0
Ki = 0.0
Kd = 10.0

last_error = 0.0
integral = 0.0

def PID_control():
    global last_error, integral
    
    error = line_position
    print(f"Error: {error}")
    
    integral += error
    derivative = error - last_error
    last_error = error
    
    max_offset = (RIGHT_POSITION - CENTER_POSITION)
    correction = Kp * error + Ki * integral + Kd * derivative
    
    angle = CENTER_POSITION + correction * max_offset
    angle = round(angle / 2) * 2  # Round to nearest even number
    angle = max(LEFT_POSITION, min(RIGHT_POSITION, angle))
    direction_servo.angle = angle

def handle_sensors():
    PID_control()
    speed = 50 - int(abs(line_position) * 20)
    forward(speed)
    
def thread_function():
    while not finished:
        if is_running:
            handle_sensors()
        else:
            stop_motors()
            direction_servo.angle = CENTER_POSITION
            time2.sleep(0.1)

process_thread = threading.Thread(target=thread_function, daemon=True)

def start():
    direction_servo.angle = CENTER_POSITION  # Neutral position
    FORWARD_PWM.start(0)  # Start PWM with 0 duty cycle
    BACKWARD_PWM.start(0) 
    if not process_thread.is_alive():
        process_thread.start()

def cleanup():
    global finished
    pca.deinit()  # Deinitialize PCA9685
    finished = True
    stop_motors()