import libs.GPIO as GPIO
import time

TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def medir_distancia():
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
        dist = medir_distancia()
        print(f"Distancia: {dist:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Medición detenida por el usuario")
    GPIO.cleanup()