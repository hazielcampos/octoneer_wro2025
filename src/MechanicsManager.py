import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO
from libs import betterTime as time2
import threading
import time

from SensorsManager import LINE_CENTER, LINE_LEFT, LINE_RIGHT, LINE_NONE

# =========================
# constantes
# =========================
CENTER_POSITION = 42  # Posición neutral del servo
LEFT_POSITION = 32 # Posición izquierda del servo
RIGHT_POSITION = 52  # Posición derecha del servo

# =========================
# Variables de estado
# =========================
is_running = False
finished = False
def set_active(active: bool):
    global is_running
    is_running = active

# =========================
# Configuración del servo con PCA9685
# =========================
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Hz para servos
direction_servo = servo.Servo(pca.channels[0])

# =========================
# Configuración del GPIO
# =========================
FORWARD_IO = 13  # Pin GPIO para mover el motor hacia adelante
BACKWARD_IO = 12  # Pin GPIO para mover el motor hacia atrás
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

def handle_sensors():
    time.sleep(0.05)  # Simular procesamiento de sensores
def thread_function():
    while not finished:
        if is_running:
            handle_sensors()
        else:
            time2.sleep(0.1)

process_thread = threading.Thread(target=thread_function, daemon=True)

def start():
    direction_servo.angle = CENTER_POSITION  # Posición neutral del servo
    FORWARD_PWM.start(0)  # Iniciar PWM con ciclo de trabajo 0
    BACKWARD_PWM.start(0)  # Iniciar PWM con ciclo de trabajo 0
    if not process_thread.is_alive():
        process_thread.start()

def cleanup():
    global finished
    pca.deinit()  # Liberar el PCA9685
    finished = True
    stop_motors()