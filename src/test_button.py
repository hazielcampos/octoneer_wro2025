import libs.GPIO as GPIO
import time

input_io = 17  # Pin GPIO para leer el estado del sensor

GPIO.setup(input_io, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configurar el botón con pull-up

while True:
    button_state = GPIO.input(input_io)
    print("Button state:", "Pressed" if button_state == 0 else "Released")
    time.sleep(0.5)