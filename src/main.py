import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO

# =========================
# Configuración del servo con PCA9685
# =========================
# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)
# Inicializar PCA9685
pca = PCA9685(i2c)
pca.frequency = 50  # Hz para servos
# Configurar servo en canal 0
servo = servo.Servo(pca.channels[0])

# =========================
# Configuración del GPIO
# =========================

FORWARD_IO = 12  # Pin GPIO para mover el motor hacia adelante
BACKWARD_IO = 13  # Pin GPIO para mover el motor hacia atrás
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 1000)  # 1 kHz
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 1000)  # 1 kHz

def setup():
    servo.angle = 53
    FORWARD_PWM.start(0)
    BACKWARD_PWM.start(0)
    loop()
    
# =========================
# Función principal
# =========================
def loop():
    while True:
        angle = int(input("Ingrese el ángulo del servo (0-180): "))
        if 0 <= angle <= 180:
            servo.angle = angle
            print(f"Servo movido a {angle} grados.")
        else:
            print("Ángulo fuera de rango. Debe estar entre 0 y 180.")

# =========================
# Limpieza al finalizar
# =========================
def cleanup():
    GPIO.cleanup()
    pca.deinit()


try:
    setup()
    
except KeyboardInterrupt:
    print("Interrupción del usuario, deteniendo el servo.")
    cleanup()
finally:
    cleanup()
    
# =========================
# Funciones de control del motor
# =========================
def forward(speed):
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)

def backward(speed):
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)