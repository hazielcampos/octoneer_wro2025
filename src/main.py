import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from libs import GPIO
import threading
import cv2
import numpy as np

# =========================
# Configuración del servo con PCA9685
# =========================
# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)
# Inicializar PCA9685
pca = PCA9685(i2c)
pca.frequency = 50  # Hz para servos
# Configurar servo en canal 0
direction_servo = servo.Servo(pca.channels[0])

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
    return not GPIO.input(input_io)

# =========================
# Funciones de control del motor
# =========================
def forward(speed, time_duration=1):
    BACKWARD_PWM.ChangeDutyCycle(0)
    FORWARD_PWM.ChangeDutyCycle(speed)
    if time_duration  > 0:
        for _ in range(time_duration * 10):
            if not is_running:
                stop()
                break
            time.sleep(0.1)

def backward(speed, time_duration=1):
    FORWARD_PWM.ChangeDutyCycle(0)
    BACKWARD_PWM.ChangeDutyCycle(speed)
    if time_duration > 0:
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
    direction_servo.angle = 42
    FORWARD_PWM.start(0)
    BACKWARD_PWM.start(0)
    loop()

line_zone = "Center"
    
# =========================
# Hilo de comandos para el control
# =========================
is_running = False

def command_loop():
    while True:
        if is_running:
            forward(60, -1)
            if line_zone == "Left":
                direction_servo.angle = 52
            elif line_zone == "Center":
                direction_servo.angle = 42
            elif line_zone == "Right":
                direction_servo.angle = 32
            
        else: 
            time.sleep(0.1)  # Esperar si no está en ejecución
            stop()
            
command_thread = threading.Thread(target=command_loop, daemon=True)
command_thread.start()

    
# =========================
# Función principal
# =========================

video = cv2.VideoCapture(0)

def camera_loop():
    global line_zone
    while True:
        ret, frame = video.read()
        
        if not ret:
            break

        # Recortar solo la parte baja de la imagen (zona de interés)
        roi = frame[100:230, 40:640]  # ajusta según tu cámara

        # Convertir a HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Definir rango de azul marino (ajusta estos valores según tu línea real)
        lower_blue = np.array([20, 30, 40])   # H, S, V mínimos
        upper_blue = np.array([140, 255, 255])  # H, S, V máximos

        # Crear máscara
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Calcular momentos para obtener el centroide
        M = cv2.moments(mask)
        if M["m00"] > 0:  # si se detectó algo
            cx = int(M["m10"] / M["m00"])  # centroide en X

            # Determinar la zona
            if cx < 300:
                line_zone = "Left"
            elif 300 <= cx < 342:
                line_zone = "Center"
            else:
                line_zone = "Right"

            # Dibujar centroide
            cv2.circle(roi, (cx, roi.shape[0]//2), 5, (0, 255, 0), -1)
        else:
            line_zone = "None"

        # Mostrar debug
        cv2.rectangle(roi, (0, 0), (300, roi.shape[0]), (255, 0, 0), 2)
        cv2.rectangle(roi, (300, 0), (342, roi.shape[0]), (0, 0, 255), 2)
        cv2.rectangle(roi, (342, 0), (642, roi.shape[0]), (255, 255, 0), 2)

        cv2.putText(frame, f"Zona: {line_zone}", (10, 460), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Mask", mask)
        cv2.imshow("Camera Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera_thread = threading.Thread(target=camera_loop, daemon=True)
camera_thread.start()

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
    video.release()
    cv2.destroyAllWindows()


try:
    setup()
    
except KeyboardInterrupt:
    print("Interrupción del usuario, deteniendo el servo.")
finally:
    cleanup()
    
