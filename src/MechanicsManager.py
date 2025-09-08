import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO
from libs import betterTime as time2
import threading
import time

import SensorsManager
# =========================
# Constants
# =========================
CENTER_POSITION = 41  # Neutral position of the servo
LEFT_POSITION = 31 # Left position of the servo
RIGHT_POSITION = 51  # Right position of the servo

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
    
def normalize_angle(angle):
    """Normaliza un ángulo a [0, 360)."""
    return angle % 360

def signed_angle_diff(current, previous):
    """
    Diferencia entre dos ángulos (con signo).
    Devuelve valores en el rango (-180, 180].
    """
    diff = (current - previous + 180) % 360 - 180
    return diff

def turn_degrees(turn_target):
    """
    Gira estrictamente en la dirección de turn_target.
    turn_target > 0 → horario (derecha).
    turn_target < 0 → antihorario (izquierda).
    """
    start_angle = normalize_angle(SensorsManager.yaw)
    previous_angle = start_angle
    accumulated = 0

    while True:
        current_angle = normalize_angle(SensorsManager.yaw)
        step = signed_angle_diff(current_angle, previous_angle)

        # Solo acumula en la dirección correcta
        if (turn_target > 0 and step > 0) or (turn_target < 0 and step < 0):
            accumulated += step

        previous_angle = current_angle
        direction_servo.angle = RIGHT_POSITION if turn_target > 0 else LEFT_POSITION
        if abs(accumulated) >= abs(turn_target):
            break

def handle_camera() -> tuple[int, int]:
    speed = 20
    angle = CENTER_POSITION
    
    return speed, angle

def handle_sensors():
    pass
    #speed, angle = handle_camera()
    #direction_servo.angle = angle
    #forward(speed)

def main_func():
    speed = 30
    direction_servo.angle = CENTER_POSITION
    forward(speed)
    
    turn_degrees(90)
    time2.sleep(20)
    
def thread_function():
    while not finished:
        
        if is_running:
            main_func()
        else:
            stop_motors()
            direction_servo.angle = CENTER_POSITION
            time.sleep(0.1)

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