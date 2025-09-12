import Rasp.GPIO as GPIO
import mechanics as mechanics
import sensors as sensors
import time
from components.Buttton import Button

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
    mechanics.start()

def main():
    while True:
        mechanics.run(is_running)
        time.sleep(0.1)

    
try:
    main()
except KeyboardInterrupt:
    print("Interrupción del usuario, limpiando...")
except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    print("Sistema detenido correctamente.")