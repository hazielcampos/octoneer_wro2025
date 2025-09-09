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
CENTER_POSITION = 52  # Neutral position of the servo
LEFT_POSITION = 62 # Left position of the servo
RIGHT_POSITION = 42  # Right position of the servo
is_turning = False

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
FORWARD_IO = 13  # GPIO pin to move the motor forward
BACKWARD_IO = 12  # GPIO pin to move the motor backward
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

def handle_camera() -> tuple[int, int]:
    speed = 20
    angle = CENTER_POSITION
    
    return speed, angle

def handle_sensors():
    global is_turning
    if SensorsManager.STATUS == SensorsManager.TURNING:
        print("Turning")
        is_turning = True
        if SensorsManager.CURVE_TYPE == SensorsManager.CURVE_ORANGE:
            direction_servo.angle = LEFT_POSITION
        elif SensorsManager.CURVE_TYPE == SensorsManager.CURVE_BLUE:
            direction_servo.angle = RIGHT_POSITION
        time.sleep(1)
        direction_servo.angle = CENTER_POSITION
        is_turning = False
        SensorsManager.STATUS = SensorsManager.GOING_STRAIGHT
        time.sleep(0.5)

def main_func():
    speed = 30
    forward(speed)
    handle_sensors()
        
def thread_function():
    global is_turning
    while not finished:
        if is_running:
            # Mueve motores
            forward(30)
            
            # Maneja curvas sin dormir
            if SensorsManager.STATUS == SensorsManager.TURNING and not is_turning:
                print("Turning")
                is_turning = True
                if SensorsManager.CURVE_TYPE == SensorsManager.CURVE_ORANGE:
                    direction_servo.angle = LEFT_POSITION
                elif SensorsManager.CURVE_TYPE == SensorsManager.CURVE_BLUE:
                    direction_servo.angle = RIGHT_POSITION
                turning_start = time.time()
            
            # Termina giro según temporizador, sin bloquear
            if is_turning and time.time() - turning_start >= 1:
                direction_servo.angle = CENTER_POSITION
                is_turning = False
                SensorsManager.STATUS = SensorsManager.GOING_STRAIGHT
                print("Straightening")
            
            time.sleep(0.01)  # Ciclo rápido, no bloqueante
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