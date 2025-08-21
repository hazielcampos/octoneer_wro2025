import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO
import threading

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

FORWARD_IO = 13  # Pin GPIO para mover el motor hacia adelante
BACKWARD_IO = 12  # Pin GPIO para mover el motor hacia atrás
GPIO.setup(FORWARD_IO, GPIO.OUT)
GPIO.setup(BACKWARD_IO, GPIO.OUT)
FORWARD_PWM = GPIO.PWM(FORWARD_IO, 1000)  # 1 kHz
BACKWARD_PWM = GPIO.PWM(BACKWARD_IO, 1000)  # 1 kHz

# =========================
# Configuración del sensor de botón
# =========================
input_io = 17  # Pin GPIO para leer el estado del sensor
GPIO.setup(input_io, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configurar el botón con pull-up

def get_button():
    return GPIO.input(input_io)

# =========================
# Funciones de control del motor
# =========================
def forward(speed, time_duration=1):
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)
    for _ in range(time_duration * 10):
        if not is_running:
            stop()
            break
        time.sleep(0.1)

def backward(speed, time_duration=1):
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)
    for _ in range(time_duration * 10):
        if not is_running:
            stop()
            break
        time.sleep(0.1)

def stop_and_wait(time_duration=1):
    stop()
    for _ in range(time_duration * 10):
        if not is_running:
            break
        time.sleep(0.1)

def stop():
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(0)
    
# =========================
# Configuración inicial
# =========================
def setup():
    servo.angle = 42
    FORWARD_PWM.start(0)
    BACKWARD_PWM.start(0)
    loop()
    
# =========================
# Hilo de comandos para el control
# =========================
is_running = False

def command_loop():
    while True:
        if is_running:
            forward(50, 2)
        else: 
            time.sleep(0.1)  # Esperar si no está en ejecución
            
command_thread = threading.Thread(target=command_loop, daemon=True)
command_thread.start()
    
# =========================
# Función principal
# =========================
def loop():
    global is_running
    while True:
        if get_button():
            is_running = not is_running
            print("Sistema " + ("iniciado" if is_running else "detenido"))
            time.sleep(0.3)  # debounce
        
        time.sleep(0.1)
            

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
finally:
    cleanup()
    
