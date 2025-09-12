import Rasp.GPIO as GPIO
import mechanics as mechanics
import sensors as sensors
import time
from components.Buttton import Button

from components.Motor import forward, stop_motors, start as start_pwm
# =========================
# State object
# =========================
is_running = False


# =========================
# Button sensor configuration
# =========================

button = Button(17, True)

def btn_callback():
    global is_running
    is_running = not is_running
    print(is_running)

button.set_callback(btn_callback)

def start():
    start_pwm()

def main():
    while True:
        if is_running:
            mechanics.sequence()
        else:
            stop_motors()

    
try:
    start()
    time.sleep(0.3)
    main()
except KeyboardInterrupt:
    print("Interrupción del usuario, limpiando...")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Sistema detenido correctamente.")
    stop_motors()