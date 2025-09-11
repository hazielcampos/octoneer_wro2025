import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# =========================
# Configuración del servo con PCA9685
# =========================
# Inicializar I2C
i2c = busio.I2C(board.SCL, board.SDA)
# Inicializar PCA9685
pca = PCA9685(i2c, address=0x43)
pca.frequency = 50  # Hz para servos
# Configurar servo en canal 0
direction_servo = servo.Servo(pca.channels[0])

direction_servo.angle = 52  # Ajusta el ángulo inicial del servo


while True:
    input_angle = input("Ingrese el ángulo del servo (0-180) o 'q' para salir: ")
    if input_angle.lower() == 'q':
        break
    try:
        angle = int(input_angle)
        if 0 <= angle <= 180:
            direction_servo.angle = angle
            print(f"Servo ajustado a {angle} grados.")
        else:
            print("Por favor, ingrese un ángulo entre 0 y 180.")
    except ValueError:
        print("Entrada no válida. Por favor, ingrese un número entero entre 0 y 180 o 'q' para salir.")
pca.deinit()  # Liberar el PCA9685 al finalizar