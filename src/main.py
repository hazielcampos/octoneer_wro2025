import RPi.GPIO as GPIO
import time
import threading
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from control.Motor import Motor

# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Inicializar PCA9685
pca = PCA9685(i2c)
pca.frequency = 50  # Hz para servos

# Configurar servo en canal 0
servo = servo.Servo(pca.channels[0])
motor = None

def setup():
    global motor
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    motor = Motor(pin_forward=12, pin_backward=13)  # Ajusta los pines según tu conexión
    servo.angle = 50
    loop()
    
def loop():
    while True:
        motor.forward(speed=0.3)
        time.sleep(1)
        motor.backward(speed=0.3)
        time.sleep(1)
        motor.stop()
        time.sleep(1)
        servo.angle = 60  # Ajusta el ángulo del servo
        time.sleep(1)
        servo.angle = 40  # Ajusta el ángulo del servo
        time.sleep(1)
        motor.forward(speed=0.3)
        time.sleep(1)
        servo.angle = 50
        time.sleep(1)

def cleanup():
    motor.stop()
    GPIO.cleanup()
    pca.deinit()
try:
    setup()
    
except KeyboardInterrupt:
    print("Interrupción del usuario, deteniendo el servo.")
    cleanup()
finally:
    cleanup()