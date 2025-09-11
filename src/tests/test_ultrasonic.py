import libs.GPIO as GPIO
from utils.i2c_manager import i2c
import adafruit_tcs34725
import time


color_sensor = adafruit_tcs34725.TCS34725(i2c)
color_sensor.integration_time = 24
color_sensor.gain = 4
TRIG_1 = 23
ECHO_1 = 24

TRIG_2 = 6
ECHO_2 = 5
GPIO.setup(TRIG_1, GPIO.OUT)
GPIO.setup(ECHO_1, GPIO.IN)

GPIO.setup(TRIG_2, GPIO.OUT)
GPIO.setup(ECHO_2, GPIO.IN)
def medir_distancia(TRIG, ECHO):
    # Asegurarse de que TRIG esté en bajo
    GPIO.output(TRIG, False)
    time.sleep(0.0002)

    # Enviar pulso de 10 microsegundos
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Medir tiempo de ida y vuelta
    while GPIO.input(ECHO) == 0:
        inicio = time.time()

    while GPIO.input(ECHO) == 1:
        fin = time.time()

    duracion = fin - inicio
    distancia = (duracion * 34300) / 2  # velocidad del sonido = 34300 cm/s
    return distancia

try:
    while True:
        dist = medir_distancia(TRIG_1, ECHO_1)
        print(f"Distancia: {dist:.2f} cm")
        dist2 = medir_distancia(TRIG_2, ECHO_2)
        print(f"Distancia2: {dist2:.2f} cm")
        time.sleep(1)
        r, g, b, c = color_sensor.color_raw
        temp = color_sensor.color_temperature
        lux = color_sensor.lux
        print(f"Color: {r} {g} {b} {c} - {temp} - {lux}")
        

except KeyboardInterrupt:
    print("Medición detenida por el usuario")
    GPIO.cleanup()